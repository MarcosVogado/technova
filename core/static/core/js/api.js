// ============================================================
//  TechNova OS — Cliente compartilhado da API REST
//  Cuida do JWT (login, storage, refresh automático no 401),
//  da guarda de rota e dos helpers de requisição.
// ============================================================
const TechNovaAPI = (() => {
    const ACCESS_KEY = 'technova_access';
    const REFRESH_KEY = 'technova_refresh';
    const USER_KEY = 'technova_user';

    const getAccess = () => localStorage.getItem(ACCESS_KEY);
    const getRefresh = () => localStorage.getItem(REFRESH_KEY);
    const getUser = () => localStorage.getItem(USER_KEY);

    function setTokens(access, refresh) {
        if (access) localStorage.setItem(ACCESS_KEY, access);
        if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
    }

    function clear() {
        [ACCESS_KEY, REFRESH_KEY, USER_KEY].forEach(k => localStorage.removeItem(k));
    }

    function logout() {
        clear();
        window.location.href = '/login/';
    }

    async function login(username, password) {
        const resp = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        if (!resp.ok) throw new Error('Usuário ou senha inválidos.');
        const data = await resp.json();
        setTokens(data.access, data.refresh);
        localStorage.setItem(USER_KEY, username);
        return data;
    }

    async function tryRefresh() {
        const refresh = getRefresh();
        if (!refresh) return false;
        const resp = await fetch('/api/auth/refresh', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh }),
        });
        if (!resp.ok) return false;
        const data = await resp.json();
        setTokens(data.access, null);
        return true;
    }

    async function request(url, options = {}, retry = true) {
        const opts = { ...options, headers: { ...(options.headers || {}) } };
        const access = getAccess();
        if (access) opts.headers['Authorization'] = 'Bearer ' + access;
        if (opts.body && !opts.headers['Content-Type']) {
            opts.headers['Content-Type'] = 'application/json';
        }

        const resp = await fetch(url, opts);
        if (resp.status === 401 && retry) {
            if (await tryRefresh()) return request(url, options, false);
            logout();
            throw new Error('Sessão expirada.');
        }
        return resp;
    }

    function formatErrors(data) {
        if (typeof data !== 'object' || data === null) return null;
        if (data.detail) return data.detail;
        const parts = [];
        for (const [k, v] of Object.entries(data)) {
            if (k === 'status_code') continue;
            const msg = Array.isArray(v) ? v.join(' ') : v;
            parts.push(k === 'non_field_errors' ? msg : `${k}: ${msg}`);
        }
        return parts.join(' | ');
    }

    async function asError(resp) {
        let detail = 'Erro ' + resp.status;
        try { detail = formatErrors(await resp.json()) || detail; } catch (e) { /* ignore */ }
        const err = new Error(detail);
        err.status = resp.status;
        return err;
    }

    async function getJSON(url) {
        const r = await request(url);
        if (!r.ok) throw await asError(r);
        return r.json();
    }

    async function send(method, url, payload) {
        const r = await request(url, { method, body: payload ? JSON.stringify(payload) : undefined });
        if (!r.ok) throw await asError(r);
        return r.status === 204 ? null : r.json();
    }

    const post = (url, p) => send('POST', url, p);
    const put = (url, p) => send('PUT', url, p);
    const del = (url) => send('DELETE', url);

    function requireAuth() {
        if (!getAccess()) {
            window.location.href = '/login/';
            return false;
        }
        return true;
    }

    return { login, logout, getUser, getAccess, requireAuth, getJSON, post, put, del };
})();
