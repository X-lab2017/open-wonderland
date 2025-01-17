import clickhouse_connect
import pandas as pd
import time

# 定义数据库连接参数
CLICKHOUSE_HOST = 
CLICKHOUSE_PORT = 
CLICKHOUSE_USER = 
CLICKHOUSE_PASSWORD = 
CLICKHOUSE_DATABASE =

def main():
    try:
        # 创建ClickHouse客户端，设置更高的超时（例如300秒）
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            user=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE,
            apply_server_timezone=False,  # 使用UTC时间
            send_receive_timeout=300  # 设置发送和接收超时为300秒
        )

        # 测试连接是否成功
        test_query = "SELECT 1"
        test_result = client.query(test_query)

        if test_result.result_rows:
            print("成功连接到 ClickHouse 数据库！")

            # 开发者活跃度
            query = """
                select sum(issue_comment) as issue_comment,
                    sum(open_issue) as open_issue,
                    sum(open_pull) as open_pull,
                    sum(review_comment) as review_comment,
                    sum(merged_pull) as merged_pull,
                    round(sum(activity), 2) as activity
                from (
                    SELECT if(type = 'PullRequestEvent' AND action = 'closed' AND pull_merged = 1, issue_author_id,
                            actor_id)                                                                 AS actor_id,
                            countIf(type = 'IssueCommentEvent' AND action = 'created')                   AS issue_comment,
                            countIf(type = 'IssuesEvent' AND action = 'opened')                          AS open_issue,
                            countIf(type = 'PullRequestEvent' AND action = 'opened')                     AS open_pull,
                            countIf(type = 'PullRequestReviewCommentEvent' AND action = 'created')       AS review_comment,
                            countIf(type = 'PullRequestEvent' AND action = 'closed' AND pull_merged = 1) AS merged_pull,
                            sqrt(0.5252 * issue_comment + 2.2235 * open_issue + 4.0679 * open_pull + 0.7427 * review_comment +
                                2.0339 * merged_pull)                                                   AS activity
                    FROM 
                        events e
                    -- 连接 gh_user_info 表
                    INNER JOIN gh_user_info u 
                        ON e.actor_id = u.id
                    -- 连接 location_info 表
                    INNER JOIN location_info l 
                        ON u.location = l.location
                    WHERE platform = 'GitHub'
                --            AND member_type != 'Bot'
                    AND (l.country = 'China'  or l.country = 'Hong Kong' or l.country = 'Taiwan')
                    AND toDate(e.created_at) >= '2024-01-01'
                    AND toDate(e.created_at) < '2025-01-01'
                    AND type IN ('PullRequestEvent', 'IssueCommentEvent', 'IssuesEvent', 'PullRequestReviewCommentEvent',
                                    'PullRequestReviewEvent')
                    group by actor_id
                )
            """

            # 仓库活跃度
            # query = """
            #     select sum(issue_comment) as issue_comment,
            #             sum(open_issue) as open_issue,
            #             sum(open_pull) as open_pull,
            #             sum(review_comment) as review_comment,
            #             sum(merged_pull) as merged_pull,
            #             round(sum(activity), 2) as activity
            #         from (
            #             SELECT if(type = 'PullRequestEvent' AND action = 'closed' AND pull_merged = 1, issue_author_id,
            #                     actor_id)                                                                 AS actor_id,
            #                     countIf(type = 'IssueCommentEvent' AND action = 'created')                   AS issue_comment,
            #                     countIf(type = 'IssuesEvent' AND action = 'opened')                          AS open_issue,
            #                     countIf(type = 'PullRequestEvent' AND action = 'opened')                     AS open_pull,
            #                     countIf(type = 'PullRequestReviewCommentEvent' AND action = 'created')       AS review_comment,
            #                     countIf(type = 'PullRequestEvent' AND action = 'closed' AND pull_merged = 1) AS merged_pull,
            #                     sqrt(0.5252 * issue_comment + 2.2235 * open_issue + 4.0679 * open_pull + 0.7427 * review_comment +
            #                         2.0339 * merged_pull)                                                   AS activity

            #             FROM events e
            #             WHERE platform = 'Gitee'
            #         --            AND member_type != 'Bot'
            #             AND toDate(created_at) >= '2024-01-01'
            #             AND toDate(created_at) < '2025-01-01'
            #             AND type IN ('PullRequestEvent', 'IssueCommentEvent', 'IssuesEvent', 'PullRequestReviewCommentEvent',
            #                             'PullRequestReviewEvent')
            #             group by actor_id
            #         )
            # """
            # 执行查询并获取结果
            start_time = time.time()
            result = client.query(query)
            end_time = time.time()

            # 将结果转换为DataFrame
            df = pd.DataFrame(result.result_rows, columns=result.column_names)
            
            print(f"\n查询执行时间: {end_time - start_time:.2f} 秒")
            print("\n查询结果:")
            print(df)

    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    main()
