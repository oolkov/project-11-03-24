import wikipedia
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from nltk import FreqDist
from nltk.tokenize import word_tokenize
import webbrowser

while True:
    try:
        # Выбор рандомной статьи из википедии
        """
        wikipedia.set_lang("ru")
        random_article = wikipedia.random(1)
        article = wikipedia.page(random_article, auto_suggest=True, redirect=False)
        article_link = article.url
        print(f"Название статьи: {article.title} {article_link}")
        """

        # Ввод искомой статьи
        wikipedia.set_lang("ru")
        article_name = input()
        article = wikipedia.page(article_name, auto_suggest=True, redirect=False)
        article_link = article.url
        print(f"Название статьи: {article.title} {article_link}")

        webbrowser.open(article_link)

        # Парсер статьи
        parser = PlaintextParser.from_string(article.content, Tokenizer("russian"))
        tokenized_text = word_tokenize(article.content.lower())

        # LexRank -- Неконтролируемый подход к обобщению текста, основанный на оценке центральности предложений на основе графов.
        # Основная идея заключается в том, что предложения «рекомендуют» читателю другие подобные предложения.
        # Таким образом, если одно предложение очень похоже на многие другие, оно, скорее всего, будет предложением большой важности.
        Summarizer_Lex = LexRankSummarizer()
        Summary_1 = Summarizer_Lex(parser.document, 10)
        print("\nLexRank суммаризация:")
        print(' '.join([str(sentence) for sentence in Summary_1]))

        # Luhn  -- на основе частоты наиболее важных слов
        Summarizer_Luhn = LuhnSummarizer()
        Summary_2 = Summarizer_Luhn(parser.document, 10)
        print("\nLuhn суммаризация:")
        print(' '.join([str(sentence) for sentence in Summary_2]))

        # SumBasic
        SummarizerSB = SumBasicSummarizer()
        Summary_3 = SummarizerSB(parser.document, 10)
        print("\nSumBasic суммаризация:")
        print(' '.join([str(sentence) for sentence in Summary_3]))

        # Автоматическое создание списков с эвристиками для Edmundson
        FDist = FreqDist(tokenized_text)
        common_words = FDist.most_common(10)

        Bonus_words = [word for word, _ in common_words]
        Stigma_words = [word for word, _ in reversed(common_words)]
        Null_words = [word for word, _ in common_words]

        # Edmudson
        Summarizer_Ed = EdmundsonSummarizer()
        Summarizer_Ed.bonus_words = Bonus_words
        Summarizer_Ed.stigma_words = Stigma_words
        Summarizer_Ed.null_words = Null_words
        Summary_4 = Summarizer_Ed(parser.document, 10)
        print("\nEdmudson суммаризация:")
        print(' '.join([str(sentence) for sentence in Summary_4]))
        break

    # wikipedia.exceptions.PageError: (статья не существует, например, не переведена на язык запроса -- русский)
    except (wikipedia.exceptions.PageError):
        print(f"Статья не существует. Повторная попытка...")
