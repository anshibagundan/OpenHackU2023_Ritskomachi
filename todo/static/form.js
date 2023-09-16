// フォームを表示する関数
function showTagForm() {
    var overlay = document.getElementById("overlay");
    overlay.style.display = "block";
}

//フォームを閉じる
function closeTagForm() {
    var overlay = document.getElementById("overlay");
    overlay.style.display = "none";
}

//フォーム内の機能

var selectedColor = ""; // 選択した色を保存する

//newcolorボタンの処理
const newcolors = document.querySelectorAll('.newcolor');
newcolors.forEach(function (button) {
    button.addEventListener("click", function () {
        // クリックされたボタンの背景色を取得
        const buttoncolor = getComputedStyle(this).backgroundColor;

        // 他のタグボタンとの比較
        let colorConflict = false;
        document.querySelectorAll('.tag').forEach(function (tagButton) {
            if (tagButton.id !== tagID) {
                const tagColor = getComputedStyle(tagButton).backgroundColor;
                if (tagColor === buttoncolor) {
                    colorConflict = true;
                    return;
                }
            }
        });

        // 警告文を表示
        if (colorConflict) {
            alert("同じ色は選べません。");
            return; // 選択をキャンセル
        }

        newcolors.forEach(function (button) {
            button.textContent = "　　　";
        });

        button.textContent = "　✔︎　"; // クリックされたボタンにチェックマークを表示

        selectedColor = buttoncolor;
    });
});


function addButton() {
    var newID = document.getElementById("tag-id").value;
    // 他のタグボタンとの比較
    let idConflict = false;
    document.querySelectorAll('.tag').forEach(function (tagButton) {
        if (tagButton.id == newID) {
                idConflict = true;
                return;
            }
    })
    // 警告文を表示
    if (idConflict) {
        alert("同じ名前のカテゴリーは追加できません。");
        return; // 選択をキャンセル
    }
    // 新しいタグボタンを作成
    var newButton = document.createElement('button');
    newButton.id = newID;
    newButton.classList.add("tag"); // 新しいボタンにクラスを追加
    newButton.textContent = newID;
    newButton.style.backgroundColor = selectedColor;

    // タグボタンのクリックイベントリスナーを追加
    newButton.onclick = function () {
        // タグのIDを取得
        tagID = this.id;

        // すべてのタグボタンのスタイルを元に戻す
        document.querySelectorAll('.tag').forEach(function (btn) {
            btn.style.transform = 'scale(1)';
        });

        // クリックされたタグボタンのサイズを変更
        this.style.transform = 'scale(1.2)';
    }
    // 新しいタグボタンを追加
    document.getElementById('tags').appendChild(newButton);
}