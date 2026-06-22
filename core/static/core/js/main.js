// --- TECHNOVA OS INTERFACE LOGIC ---

document.addEventListener('DOMContentLoaded', () => {
    console.log("TECHNOVA_OS: Sistemas de interface online.");

    // 1. Efeito de Digitação nos Títulos Neon
    const titulos = document.querySelectorAll('.neon-title');
    titulos.forEach(titulo => {
        const textoOriginal = titulo.innerText;
        titulo.innerText = '';
        let i = 0;

        function digitar() {
            if (i < textoOriginal.length) {
                titulo.innerHTML += textoOriginal.charAt(i);
                i++;
                setTimeout(digitar, 50); // Velocidade da digitação
            }
        }
        digitar();
    });

    // 2. Feedback de Hover nos Cards (Efeito de Brilho Dinâmico)
    const cards = document.querySelectorAll('.glass-panel');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transition = "0.3s";
            card.style.transform = "scale(1.02) translateY(-5px)";
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = "scale(1) translateY(0)";
        });
    });

    // 3. Efeito Sonoro Simulado / Notificação de Botões
    const botoes = document.querySelectorAll('.btn');
    botoes.forEach(botao => {
        botao.addEventListener('click', (e) => {
            // Cria um efeito de pulso no clique
            let ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');
            botao.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // 4. Auto-hide para as mensagens de alerta (Feedback de Transação)
    //    Importante: ignora alertas escondidos (.d-none), como as caixas de erro
    //    dos formulários (#formErro), para não removê-las do DOM.
    //    O feedback global é gerenciado por window.flash() (base.html).
    const alertas = document.querySelectorAll('.alert:not(.d-none)');
    alertas.forEach(alerta => {
        setTimeout(() => {
            alerta.style.opacity = '0';
            alerta.style.transition = '1s';
            setTimeout(() => alerta.remove(), 1000);
        }, 4000); // Alerta some após 4 segundos
    });
});