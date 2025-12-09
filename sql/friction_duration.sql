WITH
EARLIEST_EVENT AS (
    SELECT
        EVENT_NAME
        , PLATFORM
        , REGION
        , EXPERIENCE
        , USER_ID
        , CASE
            WHEN EVENT_NAME = 'Transfer Created' THEN 1
            WHEN EVENT_NAME = 'Transfer Funded' THEN 2
            WHEN EVENT_NAME = 'Transfer Transferred' THEN 3
        END AS EVENT_ORDER
        -- Validates that we only take the FIRST time a user did this event
        , MIN(EVENT_DATE) AS FIRST_EVENT_DATE
    FROM TRANSACTIONS -- noqa: RF04
    GROUP BY
        EVENT_NAME
        , PLATFORM
        , REGION
        , EXPERIENCE
        , USER_ID
)

, INTER_STAGE_FRICTION AS (
    SELECT
        EVENT_NAME
        , PLATFORM
        , REGION
        , EXPERIENCE
        , USER_ID
        , FIRST_EVENT_DATE
        -- Get the timestamp of the previous stage for this specific user
        , LAG(FIRST_EVENT_DATE) OVER (
            PARTITION BY PLATFORM, REGION, EXPERIENCE, USER_ID
            ORDER BY EVENT_ORDER
        ) AS PREVIOUS_EVENT_DATE
    FROM EARLIEST_EVENT
)

, AVG_FRICTION AS (
    SELECT
        PLATFORM
        , REGION
        , EXPERIENCE
        , USER_ID
        , CASE
            WHEN EVENT_NAME = 'Transfer Funded' THEN 'Transfer Created → Transfer Funded'
            WHEN EVENT_NAME = 'Transfer Transferred' THEN 'Transfer Funded → Transfer Transferred'
        END AS EVENT_NAME
        , FIRST_EVENT_DATE - PREVIOUS_EVENT_DATE AS FRICTION
    FROM INTER_STAGE_FRICTION
    WHERE PREVIOUS_EVENT_DATE IS NOT NULL -- Only look at rows where there was a previous stage
)

SELECT
    EVENT_NAME
    , PLATFORM
    , REGION
    , EXPERIENCE
    , USER_ID
    , FRICTION
FROM AVG_FRICTION
ORDER BY
    EVENT_NAME
    , PLATFORM
    , REGION
    , USER_ID
    , EXPERIENCE;
