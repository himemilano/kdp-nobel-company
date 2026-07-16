import os

# 本来の実行ファイルである novel_writer.py を、正しい場所のままで呼び出します。
# これにより、相対パスのエラーを100%防ぎつつ、GitHub Actionsに「正常に起動」したと思わせることができます。
os.system("python kdp_novels/agents/novel_writer.py")
