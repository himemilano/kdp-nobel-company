import os
import sys
import subprocess

def main():
    print("🚀 [KDP Project Central] 統括システム（社長）を起動します...")

    # 🔑 【最終防衛ライン】環境変数の存在チェック
    api_key = os.environ.get("KDP_GEMINI_API_KEY")
    if not api_key:
        print("\n❌ [社長の激怒] 環境変数 'KDP_GEMINI_API_KEY' が設定されていません！")
        print("GitHub ActionsのSecrets、またはローカルの環境変数を確認してください。")
        print("安全のため、全マシーンの稼働を強制停止します。")
        sys.exit(1)

    # 🏃‍♂️ 【黄金のパイプライン】一本道のリレー順序
    # ※各スクリプトの配置フォルダ（kdp_novels/agents/）に合わせてパスを設定しています。
    agents = [
        ("🕵️‍♂️ 市場調査部門", "kdp_novels/agents/market_researcher.py"),
        ("📐 プロット設計部門", "kdp_novels/agents/plot_designer.py"),
        ("💰 SEOマーケティング部門", "kdp_novels/agents/seo_marketer.py"),
        ("✍️ 小説執筆部門", "kdp_novels/agents/novel_writer.py"),
        ("🛡️ 法務監査部門", "kdp_novels/agents/legal_compliance_checker.py"),
    ]

    print("\n--- ⚙️ パイプライン・リレーを開始します（無限ループなし・One-Shot設計） ---")
    
    for index, (name, script_path) in enumerate(agents, 1):
        print(f"\n▶️ 【Step {index}: {name}】を招集... ({script_path})")
        
        # ファイルが物理的に存在するか確認
        if not os.path.exists(script_path):
            print(f"❌ [致命的エラー] スクリプトファイルが指定のパスに見つかりません: {script_path}")
            print("フォルダ構成やファイル名が正しいか確認してください。リレーを中止します。")
            sys.exit(1)
            
        try:
            # 🛡️ check=True により、子スクリプトの異常終了(sys.exit(1))を確実に検知して例外を発生させる
            subprocess.run(["python", script_path], check=True)
            print(f"✨ 【{name}】が正常にタスクを完了、または資産を保護して退勤しました。")
            
        except subprocess.CalledProcessError as e:
            print(f"\n🚨 [緊急停止] 【{name}】の処理中に重大なエラーが発生しました（終了コード: {e.returncode}）。")
            print("これ以上のAPI代の浪費とファイル破損を防ぐため、ここで全システムを安全に緊急停止します。")
            print("GitHub Actionsのログを確認し、原因（API制限やコードエラーなど）を特定してください。")
            sys.exit(1)

    print("\n==================================================")
    print("🎉 [ミッション完了] 本日のパブリッシング・リレーがすべて安全に終了しました！")
    print("成果物は 'kdp_novels/workspace/' を確認してください。")
    print("お疲れ様でした！次回のスケジュール起動までシステムは完全スリープします（維持費 ¥0）。")
    print("==================================================")

if __name__ == "__main__":
    main()
