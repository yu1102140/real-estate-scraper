# 不動産データのスクレイピング
こちらの案件を参考に関西の不動産データのみスクレイピングを行いました。

https://crowdworks.jp/public/jobs/12201726

RealEstate_kansai_search.pyではSeleniumを用いて、物件検索条件の選択、検索結果の全ページのhtmlの取得を行いました。
htmlフォルダに各ページhtmlを格納しています。

RealEstate_scraping.pyではBeautifulsoupを用いて各ページhtmlから必要な項目を抽出、real_estate_data.csvに出力しています。
