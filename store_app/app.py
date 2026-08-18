// 巨大な画像データを一括消去してJSONBinのロックを解除するコマンド
fetch('/api/get_all_data')
  .then(res => res.json())
  .then(data => {
    if (data.forum) {
      data.forum.forEach(post => delete post.image);
    }
    return fetch('/api/save_all_data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  })
  .then(res => res.json())
  .then(res => {
    alert("容量の解放が完了しました！ページをリロードしてください。");
    location.reload();
  })
  .catch(err => alert("エラー: " + err));
