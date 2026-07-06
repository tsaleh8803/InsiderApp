from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./insider_app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class ArticleAnalysis(Base):
    __tablename__ = "article_analysis"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    title = Column(String)
    publisher = Column(String)
    link = Column(String)
    sentiment = Column(String)
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


def create_tables():
    Base.metadata.create_all(bind=engine)


def save_article_analysis(ticker, article):
    db = SessionLocal()

    saved_article = ArticleAnalysis(
        ticker=ticker,
        title=article["title"],
        publisher=article["publisher"],
        link=article["link"],
        sentiment=article["sentiment"],
        score=article["score"]
    )

    db.add(saved_article)
    db.commit()
    db.refresh(saved_article)
    db.close()

    return saved_article


def get_history(ticker):
    db = SessionLocal()

    results = (
        db.query(ArticleAnalysis)
        .filter(ArticleAnalysis.ticker == ticker.upper())
        .order_by(ArticleAnalysis.created_at.desc())
        .all()
    )

    db.close()

    return results