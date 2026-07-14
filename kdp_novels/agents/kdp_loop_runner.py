import os
import sys
import time
import subprocess
from datetime import datetime, timedelta, timezone

# 日本時間設定
jst = timezone(timedelta(hours=9))

# 実行ターゲット：kdp_novels/agents/ 直下の5大エージェント（相対パスを完全に適合させています）
SCRIPTS_TO_RUN = [
    "kdp_novels/agents/market_researcher.py",         # 1. 市場調査
    "kdp_novels/agents/plot_designer.py",             # 2. プロット設計
    "kdp_novels/agents/novel_writer.py",              # 3. 本文執筆
    "kdp_novels/agents/seo_marketer.py",              # 4. タイトル・紹介文
    "kdp_novels/agents/legal_compliance_checker.py"   # 5. 重複・規約チェック
]

# APIリミットセーフガード (1分間の最大リクエスト数12回：約5秒に1回の間隔)
MAX_REQUESTS_PER_MINUTE = 12
REQUEST_INTERVAL = 60 / MAX_REQUESTS_PER_MINUTE

def run_script_safely(script_path):
    if not os.path.exists(script_path):
        print(f"⚠️ スクリプトが見つかりません: {script_path} (スキップします)")
        return False
        
    current_time = datetime.now(jst).strftime("%H:%M:%S")
    print(f"\n[🔄 KDPループ実行] {current_time} - {script_path} を開始...")
    
    start_time = time.time()
    try:
        # プロセスとしてエージェントを順次起動
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=300)
        
        print(result.stdout)
        if result.stderr:
            print(f"❌ エラー出力:\n{result.stderr}")
            
        elapsed = time.time() - start_time
        print(f"⏱️ 完了 (処理時間: {elapsed:.1f}秒)")
        
        # API保護待機
        time.sleep(REQUEST_INTERVAL)
        return True
    except subprocess.TimeoutExpired:
        print(f"⚠️ 5分以上応答がないためタイムアウトしました: {script_path}")
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
            print("⏳ コンテナ制限時間に達したため、次の枠へループをバトンタッチします。")
            break
            
        run_count += 1
        print(f"\n--- 📚 第 {run_count} 回目の小説生成・市場監視ループ ---")
        
        # 5つのエージェントを順に実行
        for script in SCRIPTS_TO_RUN:
            run_script_safely(script)
            
        # 1サイクル完了ごとに30秒待機
        time.sleep(30)
        
        # workspaceフォルダ等に生成された最新原稿（マークダウンなど）を検知してGitHubへプッシュ
        try:
            subprocess.run(["git", "config", "--local", "user.email", "action@github.com"], capture_output=True)
            subprocess.run(["git", "config", "--local", "user.name", "GitHub Action"], capture_output=True)
            subprocess.run(["git", "add", "."], capture_output=True)
            
            status_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if status_res.stdout.strip():
                print("📦 新規小説原稿・報告書の書き出しを検知！自動でコミット・プッシュします...")
                subprocess.run(["git", "commit", "-m", "📚 [KDP-Autonomy] 24時間自律ループにより最新小説原稿を自動プッシュ"], capture_output=True)
                subprocess.run(["git", "push"], capture_output=True)
        except Exception as e:
            print(f"⚠️ 自動コミット例外: {e}")

if __name__ == "__main__":
    main()

