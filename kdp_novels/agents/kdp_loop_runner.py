import os
import sys
import time
import subprocess
from datetime import datetime, timedelta, timezone

# 日本時間設定
jst = timezone(timedelta(hours=9))

# 📚 小説生成プロセスの5大エージェントを自動巡回
SCRIPTS_TO_RUN = [
    "kdp_novels/agents/market_researcher.py",         # 1. 市場調査・トレンド分析
    "kdp_novels/agents/plot_designer.py",             # 2. プロット・キャラクター設計
    "kdp_novels/agents/novel_writer.py",              # 3. 本文の執筆・自動生成
    "kdp_novels/agents/seo_marketer.py",              # 4. タイトル・紹介文・SEO設計
    "kdp_novels/agents/legal_compliance_checker.py"   # 5. 法的規約・重複チェック
]

# APIリミットセーフガード (1分間の最大リクエスト数を12回に自主規制してエラーを回避)
MAX_REQUESTS_PER_MINUTE = 12
REQUEST_INTERVAL = 60 / MAX_REQUESTS_PER_MINUTE # 5秒インターバル

def run_script_safely(script_path):
    if not os.path.exists(script_path):
        return False
        
    current_time = datetime.now(jst).strftime("%H:%M:%S")
    print(f"\n[🔄 KDPループ実行] {current_time} - {script_path} を開始...")
    
    start_time = time.time()
    try:
        # エージェントスクリプトを外部プロセスとして起動
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=300)
        
        print(result.stdout)
        if result.stderr:
            print(f"❌ エラー出力:\n{result.stderr}")
            
        elapsed = time.time() - start_time
        print(f"⏱️ 完了 (処理時間: {elapsed:.1f}秒)")
        
        # API安全マージン待機
        time.sleep(REQUEST_INTERVAL)
        return True
    except subprocess.TimeoutExpired:
        print(f"⚠️ タイムアウト(5分超過により強制打ち切り): {script_path}")
        return False
    except Exception as e:
        print(f"❌ 実行エラー: {e}")
        return False

def main():
    print("==========================================================")
    print("🔥 KDP Novel Publisher 自律常時限界ループランナー 🔥")
    print("==========================================================")
    
    loop_start_time = time.time()
    max_loop_duration = 5 * 60 * 60 + 40 * 60 # 5時間40分間、常時コンテナ内で執筆をループ
    
    run_count = 0
    while True:
        elapsed_total = time.time() - loop_start_time
        if elapsed_total > max_loop_duration:
            print("⏳ GitHub Actionsの制限（6時間）に近いため、次の枠へループをバトンタッチします。")
            break
            
        run_count += 1
        print(f"\n--- 📚 第 {run_count} 回目の小説生成・市場監視ループ ---")
        
        # 登録エージェントを順次実行
        for script in SCRIPTS_TO_RUN:
            run_script_safely(script)
            
        # 執筆負荷を考慮して30秒息抜き
        time.sleep(30)
        
        # 出来上がった小説のプロット、執筆原稿（workspace等）をGitHubに自律プッシュ
        try:
            subprocess.run(["git", "config", "--local", "user.email", "action@github.com"], capture_output=True)
            subprocess.run(["git", "config", "--local", "user.name", "GitHub Action"], capture_output=True)
            subprocess.run(["git", "add", "."], capture_output=True)
            
            status_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if status_res.stdout.strip():
                print("📦 新規書き下ろし原稿の更新を検知！自動でコミット・プッシュします...")
                subprocess.run(["git", "commit", "-m", "📚 [KDP-Autonomy] 小説原稿の最新執筆パートを自律格納しました"], capture_output=True)
                subprocess.run(["git", "push"], capture_output=True)
        except Exception as e:
            print(f"⚠️ 自動コミット例外: {e}")

if __name__ == "__main__":
    main()

