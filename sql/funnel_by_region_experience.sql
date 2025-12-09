WITH
USER_COUNT AS (
    SELECT
        EVENT_NAME
        , REGION
        , EXPERIENCE
        , COUNT(DISTINCT USER_ID) AS USER_COUNT
    FROM TRANSACTIONS -- noqa: RF04
    GROUP BY
        EVENT_NAME
        , REGION
        , EXPERIENCE
)

, FUNNEL_STAGES AS (
    SELECT
        EVENT_NAME
        , REGION
        , EXPERIENCE
        , USER_COUNT
        -- Add stage ordering based on typical funnel progression
        , CASE
            WHEN EVENT_NAME = 'Transfer Created' THEN 1
            WHEN EVENT_NAME = 'Transfer Funded' THEN 2
            WHEN EVENT_NAME = 'Transfer Transferred' THEN 3
        END AS EVENT_ORDER
    FROM USER_COUNT
)

, CONVERSION_AND_DROP_OFF_RATES AS (
    SELECT
        EVENT_NAME
        , REGION
        , EXPERIENCE
        , USER_COUNT
        , EVENT_ORDER
        , NULLIF(LAG(USER_COUNT)
            OVER (PARTITION BY REGION, EXPERIENCE ORDER BY EVENT_ORDER), 0)
            AS PREV_STAGE_COUNT
        , ROUND(
            USER_COUNT
            / NULLIF(
                LAG(USER_COUNT)
                    OVER (PARTITION BY REGION, EXPERIENCE ORDER BY EVENT_ORDER)
                , 0
            )
            , 2
        ) AS CONVERSION_RATE
        , ROUND(
            (
                LAG(USER_COUNT)
                    OVER (PARTITION BY REGION, EXPERIENCE ORDER BY EVENT_ORDER)
                - USER_COUNT
            )
            / NULLIF(
                LAG(USER_COUNT)
                    OVER (PARTITION BY REGION, EXPERIENCE ORDER BY EVENT_ORDER)
                , 0
            )
            , 2
        ) AS DROP_OFF_RATE
        , ROUND(
            USER_COUNT
            / NULLIF(
                FIRST_VALUE(USER_COUNT)
                    OVER (PARTITION BY REGION, EXPERIENCE ORDER BY EVENT_ORDER)
                , 0
            )
            , 2
        ) AS CUMULATIVE_CONVERSION_RATE
    FROM FUNNEL_STAGES
)

SELECT
    EVENT_NAME
    , REGION
    , EXPERIENCE
    , USER_COUNT
    , PREV_STAGE_COUNT
    , CONVERSION_RATE
    , DROP_OFF_RATE
    , CUMULATIVE_CONVERSION_RATE
FROM CONVERSION_AND_DROP_OFF_RATES
ORDER BY
    REGION
    , EXPERIENCE
    , EVENT_ORDER;
