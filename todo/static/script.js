// ボタン要素とメニューバー要素を取得
const toggleButton = document.getElementById('toggle-button');
const menuBar = document.getElementById('menu-bar');

// ボタンをクリックしたときの動作を設定
toggleButton.addEventListener('click', () => {
    // メニューバーの表示状態を切り替える
    if (menuBar.style.display === 'none' || menuBar.style.display === '') {
        menuBar.style.display = 'block'; // メニューバーを表示
        toggleButton.textContent = 'メニューを非表示'; // ボタンのテキストを変更
    } else {
        menuBar.style.display = 'none'; // メニューバーを非表示
        toggleButton.textContent = 'メニューを表示'; // ボタンのテキストを変更
    }
});
