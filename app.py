if st.button("Collect & Analyze"):
    if keyword.strip() == "":
        st.warning("אנא הזן מילה או תחום לחיפוש.")
    else:
        st.write(f"מחפש בעיות עם מילת מפתח: **{keyword}** ...")

        reddit_df = fetch_reddit_posts(["BuyItForLife", "LifeProTips"], days=7)
        trends_df = fetch_google_trends()
        tiktok_df = fetch_websearch(keyword, site="tiktok.com")
        quora_df = fetch_websearch(keyword, site="quora.com")

        combined = merge_and_filter([reddit_df, trends_df, tiktok_df, quora_df])
        if combined.empty:
            st.warning("לא נמצאו בעיות עם מילת המפתח הזו.")
        else:
            # ---- Limit to Top 1 problem to save tokens ----
            top_problem = combined.iloc[0]["text_clean"]
            st.write(f"### Top Problem Selected:\n{top_problem}")

            # ---- GPT Analysis (one time only) ----
            gpt_result = analyze_problem(top_problem)
            st.write("**GPT raw output:**", gpt_result)

            results = []
            for line in gpt_result.split("\n"):
                if "Product" in line and "|" in line:
                    try:
                        product_name = line.split("|")[0].split(":")[1].strip()
                        score = line.split("|")[1].split(":")[1].replace("%", "").strip()
                    except Exception:
                        continue

                    link = search_aliexpress(product_name)
                    if not link:
                        link = f"https://www.aliexpress.com/wholesale?SearchText={product_name.replace(' ', '%20')}"
                    results.append({
                        "problem": top_problem,
                        "product": product_name,
                        "match_percent": score,
                        "aliexpress_link": f"[Link]({link})"
                    })

            output_df = pd.DataFrame(results)
            st.markdown(output_df.to_markdown(index=False), unsafe_allow_html=True)
            st.download_button("Download CSV", output_df.to_csv(index=False), "output.csv")
