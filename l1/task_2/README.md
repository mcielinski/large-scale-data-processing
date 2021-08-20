# L1 - 2019

## Task 2
Proof that you can use Vim:
- find an expression
  ```text
  Answer:
  1. if in INSERT mode - hit 'ESC'
  2. type '/' (search forward) or '?' (search backward) and enter the search pattern </word>
  3. use 'n' to find the next occurrence or 'N' to search in backwards
  ```
- jump to line
  ```text
  Answer:
  3 ways:
    - <line>gg
    - <line>G
    - :<line><CR>
  ```
- substitute a single character
  ```text
  Answer:
  's' then the sign you want to replace with
  [e.g.
    before: give
    highlight 'g'
    type: 's''l' -> 'ESC'
    after: live
  ]
  you can replace more than one character by specifying their number
  [e.g.
    before: give_me
    highlight 'g'
    type: '4s''hug' -> 'ESC'
    after: hug_me
  ]
  ```
- substitute a whole expression
  ```text
  Answer:
  - find each occurrence in current line of 'word' and replace it with 'new_word':
    :s/word/new_word/g
  
  - find each occurrence of 'word'...:
    :%s/word/new_word/g
  ```
- save changes
  ```text
  Answer:
  :w
  ```
- exit Vim (2 ways)
  ```text
  Answer:
  save and quit:
    - :x
    - :wq
    - 'SHIFT' + 'ZZ'
  discord changes and quit:
    - :q!
    - 'SHIFT' + 'ZX'
  ```
  