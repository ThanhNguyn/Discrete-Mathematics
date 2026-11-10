"""Dự án 1.2 - Công cụ tìm kiếm mini cho bài báo tiếng Việt."""
from __future__ import annotations

from collections import Counter, defaultdict
import math
import re
import unicodedata


STOP_WORDS = {
    "va", "la", "cua", "cho", "mot", "nhung", "trong", "voi", "cac",
    "duoc", "tu", "nay", "den", "co", "khong", "tren", "nhu",
}


def tach_tu(text: str) -> list[str]:
    normalized = "".join(
        character
        for character in unicodedata.normalize("NFD", text).casefold()
        if unicodedata.category(character) != "Mn"
    )
    words = re.findall(r"[^\W\d_]+", normalized, flags=re.UNICODE)
    return [word for word in words if word not in STOP_WORDS and len(word) > 1]


class InvertedIndex:
    def __init__(self, articles=()):
        self.articles = {}
        self.postings = defaultdict(dict)
        self.document_frequency = Counter()
        for article_id, text in articles:
            self.them_bai_bao(article_id, text)

    def them_bai_bao(self, article_id, text: str) -> None:
        if not article_id or article_id in self.articles:
            raise ValueError("article_id phải khác rỗng và không trùng")
        words = tach_tu(text)
        self.articles[article_id] = text
        frequencies = Counter(words)
        for word, frequency in frequencies.items():
            self.postings[word][article_id] = frequency
        self.document_frequency.update(frequencies.keys())

    def tim_kiem(self, query: str, mode: str = "AND", limit: int = 10):
        terms = list(dict.fromkeys(tach_tu(query)))
        if not terms:
            return []
        if mode not in {"AND", "OR"}:
            raise ValueError("mode phải là AND hoặc OR")
        found = [
            set(self.postings.get(term, {}))
            for term in terms
        ]
        matching = set.intersection(*found) if mode == "AND" else set.union(*found)
        scores = []
        total_documents = len(self.articles)
        for article_id in matching:
            score = 0.0
            for term in terms:
                frequency = self.postings[term].get(article_id, 0)
                if frequency:
                    idf = math.log((1 + total_documents) / (1 + self.document_frequency[term])) + 1
                    score += (1 + math.log(frequency)) * idf
            scores.append((score, article_id, self.articles[article_id]))
        scores.sort(key=lambda result: (-result[0], result[1]))
        return scores[:limit]


BAI_BAO_MAU = (
    ("python", "Python hỗ trợ phân tích dữ liệu và xây dựng ứng dụng web."),
    ("ai", "Trí tuệ nhân tạo và học máy đang thay đổi nhiều ngành công nghiệp."),
    ("csdl", "Cơ sở dữ liệu giúp lưu trữ và tìm kiếm dữ liệu hiệu quả."),
)


if __name__ == "__main__":
    index = InvertedIndex(BAI_BAO_MAU)
    print(index.tim_kiem("dữ liệu"))
    print(index.tim_kiem("python web", mode="OR"))
