INSERT INTO
    QA (question, answer)
VALUES
    (
        'What is the latest block?',
        'The latest block count is 2928390.'
    ),
    (
        'How many DFI do I need to create a masternode?',
        'Currently, you need a minimum of 20,000 DFI to create a masternode on DeFiChain. However, it is possible to use a service provider to stake less than that amount.'
    ),
    (
        'What is the current supply of DFI?',
        'The current total supply of DFI is 546,205,671 DFI.'
    );

INSERT INTO
    users (user_token)
VALUES
    ('1234567890'),
    ('1234567891'),
    ('1234567892');

INSERT INTO
    chat_messages (user_id, message_type, content, timestamp)
VALUES
    (
        1,
        'human',
        'Hi',
        CURRENT_DATE + INTERVAL '10:00:00' HOUR TO SECOND
    ),
    (
        1,
        'jelly',
        'Hello, how can I help you?',
        CURRENT_DATE + INTERVAL '10:00:02' HOUR TO SECOND
    ),
    (
        1,
        'human',
        'What is the latest block?',
        CURRENT_DATE + INTERVAL '10:00:05' HOUR TO SECOND
    ),
    (
        1,
        'tool',
        'Let me gather the latest blockchain statistics for you 📊',
        CURRENT_DATE + INTERVAL '10:00:07' HOUR TO SECOND
    ),
    (
        1,
        'jelly',
        'The latest block count is 2928390.',
        CURRENT_DATE + INTERVAL '10:00:10' HOUR TO SECOND
    ),
    (
        1,
        'human',
        'Thank you!',
        CURRENT_DATE + INTERVAL '10:01:12' HOUR TO SECOND
    ),
    (
        1,
        'jelly',
        'You are welcome. If there is anything else I can help you with, feel free to ask.',
        CURRENT_DATE + INTERVAL '10:01:14' HOUR TO SECOND
    ),
    (
        2,
        'human',
        'Hi',
        CURRENT_DATE + INTERVAL '10:00:20' HOUR TO SECOND
    ),
    (
        2,
        'jelly',
        'Hello, how can I help you?',
        CURRENT_DATE + INTERVAL '10:00:22' HOUR TO SECOND
    ),
    (
        2,
        'human',
        'How many DFI do I need to create a masternode?',
        CURRENT_DATE + INTERVAL '10:00:25' HOUR TO SECOND
    ),
    (
        2,
        'tool',
        'Ill go look this up in the DeFiChainWiki for you 🔎',
        CURRENT_DATE + INTERVAL '10:00:27' HOUR TO SECOND
    ),
    (
        2,
        'jelly',
        'Currently, you need a minimum of 20,000 DFI to create a masternode on DeFiChain. However, it is possible to use a service provider to stake less than that amount.',
        CURRENT_DATE + INTERVAL '10:00:34' HOUR TO SECOND
    ),
    (
        2,
        'human',
        'Thank you!',
        CURRENT_DATE + INTERVAL '10:01:36' HOUR TO SECOND
    ),
    (
        2,
        'jelly',
        'You are welcome. If there is anything else I can help you with, feel free to ask.',
        CURRENT_DATE + INTERVAL '10:01:38' HOUR TO SECOND
    ),
    (
        3,
        'human',
        'Hi',
        CURRENT_DATE + INTERVAL '12:00:00' HOUR TO SECOND
    ),
    (
        3,
        'jelly',
        'Hello, how can I help you?',
        CURRENT_DATE + INTERVAL '12:00:02' HOUR TO SECOND
    ),
    (
        3,
        'human',
        'What is the current supply of DFI?',
        CURRENT_DATE + INTERVAL '12:00:04' HOUR TO SECOND
    ),
    (
        3,
        'tool',
        'Let me gather the latest blockchain statistics for you 📊',
        CURRENT_DATE + INTERVAL '12:00:06' HOUR TO SECOND
    ),
    (
        3,
        'jelly',
        'The current total supply of DFI is 546,205,671 DFI.',
        CURRENT_DATE + INTERVAL '12:00:09' HOUR TO SECOND
    ),
    (
        3,
        'human',
        'Thank you!',
        CURRENT_DATE + INTERVAL '12:01:12' HOUR TO SECOND
    ),
    (
        3,
        'jelly',
        'You are welcome. If there is anything else I can help you with, feel free to ask.',
        CURRENT_DATE + INTERVAL '12:01:14' HOUR TO SECOND
    );