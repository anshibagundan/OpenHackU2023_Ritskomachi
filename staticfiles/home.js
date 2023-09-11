// JavaScriptでボタン要素とモーダル要素を取得
const btnTriggers = document.querySelectorAll('.btn-trigger');
const masks = document.querySelectorAll('[id^="mask"]');
const modals = document.querySelectorAll('[id^="modal"]');

// 各ボタンにクリックイベントを設定
btnTriggers.forEach((btn, index) => {
    btn.addEventListener('click', () => {
        masks[index].classList.remove('hidden');
        modals[index].classList.remove('hidden');
    });
});

// 各マスクをクリックしたときにモーダルを隠す
masks.forEach((mask, index) => {
    mask.addEventListener('click', () => {
        mask.classList.add('hidden');
        modals[index].classList.add('hidden');
    });
});

