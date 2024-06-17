from cleantext import clean


def clean_text(raw_text: str) -> str:
    return clean(raw_text,
          fix_unicode=True,               # fix various unicode errors
          to_ascii=False,                  # transliterate to closest ASCII representation
          lower=False,                     # lowercase text
          # fully strip line breaks as opposed to only normalizing them
          no_line_breaks=False,
          keep_two_line_breaks=False,
          strip_lines=True,
          no_urls=False,                   # replace all URLs with a special token
          no_emails=False,                 # replace all email addresses with a special token
          no_phone_numbers=False,          # replace all phone numbers with a special token
          no_numbers=False,                # replace all numbers with a special token
          no_digits=False,                # replace all digits with a special token
          no_currency_symbols=False,      # replace all currency symbols with a special token
          no_punct=False,                 # remove punctuations
          lang="en"                       # set to 'de' for German special handling
          )
