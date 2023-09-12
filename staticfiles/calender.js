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
// ボタン要素とメニューバー要素を取得
const taskButtons = document.querySelectorAll('#task-button');
const taskBars = document.querySelectorAll('#task-bar');
const calenderSlide = document.querySelector('#content-wrapper');


taskButtons.forEach((taskButton, index) => {
    taskButton.addEventListener("click", () => {
        // メニューバーの表示状態を切り替える
        if (taskBars[index].style.display === 'none' || taskBars[index].style.display === '') {
            taskBars[index].style.display = 'block'; // メニューバーを表示
            calenderSlide.style.marginRight = '30%';
            taskButton.textContent = day.day; // ボタンのテキストを変更
        } else {
            taskBars[index].style.display = 'none'; // メニューバーを非表示
            calenderSlide.style.marginRight = '0%';
            taskButton.textContent = day.day; // ボタンのテキストを変更
        }
    });
});
// チェックボックス要素の取得
const checkboxes = document.querySelectorAll('.checkbox');

// 各チェックボックスにクリックイベントリスナーを追加
checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('click', () => {
        checkbox.classList.toggle('checked');
        const isChecked = checkbox.classList.contains('checked');
        checkbox.setAttribute('data-checked', isChecked ? 'true' : 'false');
    });
});
