import React, { useState, useEffect } from 'react';
import './ArticleFetcher.css'; // Ensure this path is correct

function ArticleFetcher() {
    const [fetchInterval, setFetchInterval] = useState(20); // Default to 20 seconds
    const [articles, setArticles] = useState([]);
    const [timeLeft, setTimeLeft] = useState(fetchInterval);
    const [showNoArticlesMessage, setShowNoArticlesMessage] = useState(false);
    const [messageOpacity, setMessageOpacity] = useState(0);
    const [selectedArticleDetails, setSelectedArticleDetails] = useState(null);
    const [selectedArticleUrl, setSelectedArticleUrl] = useState(null);



    // Fetch articles from backend
    const [existingArticles, setExistingArticles] = useState([]);

    const fetchInitialData = async () => {
        try {
            const response = await fetch('http://localhost:8000/links');
            const initialData = await response.json();
            setArticles(initialData.map(article => ({
                ...article,
                detailsVisible: false // Add visibility flag
            })));
        } catch (error) {
            console.error('Error fetching initial data:', error);
        }
    };

    useEffect(() => {
        fetchInitialData();
        // Start the timer after initial data is loaded
        const interval = setInterval(() => {
            setTimeLeft(prevTimeLeft => prevTimeLeft > 0 ? prevTimeLeft - 1 : 0);
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    const fetchArticles = async () => {
        try {
            const response = await fetch(`http://localhost:8000/parse_links?limit=100`);
            const newData = await response.json();

            if (Array.isArray(newData) && newData.length > 0) {
                const timestampedNewData = newData.map(article => ({
                    ...article,
                    isNew: true,
                    detailsVisible: false // Add visibility flag
                }));
                setArticles(prevArticles => [...timestampedNewData, ...prevArticles]);
            } else {
                setShowNoArticlesMessage(true); // Show the message
                setMessageOpacity(1); // Set opacity to 1 to show the message
                setTimeout(() => {
                    setShowNoArticlesMessage(false);
                    setMessageOpacity(0); // Set opacity back to 0 after 2 seconds
                }, 2000);
            }
        } catch (error) {
            console.error("Error fetching articles:", error);
        }
        setTimeLeft(fetchInterval);
    };

    // Fetch articles whenever the timer reaches zero
    useEffect(() => {
        if (timeLeft === 0) {
            fetchArticles();
        }
    }, [timeLeft]);

    // Handler for slider change
    const handleSliderChange = (e) => {
        const newInterval = Number(e.target.value);
        setFetchInterval(newInterval);
        setTimeLeft(newInterval); // Reset the countdown
    };

    function decodeHtml(html) {
        var txt = document.createElement("textarea");
        txt.innerHTML = html;
        return txt.value;
    }

    const handleArticleDetails = async (articleUrl, index) => {
        const newArticles = [...articles];
        const article = newArticles[index];

        // Toggle visibility
        article.detailsVisible = !article.detailsVisible;

        // Fetch details if not already fetched
        if (!article.content && article.detailsVisible) {
            try {
                const encodedUrl = encodeURIComponent(articleUrl);
                const response = await fetch(`http://localhost:8000/parse_article?article_url=${encodedUrl}`);
                const articleDetails = await response.json();
                article.content = articleDetails.content; // Store the content in the article
            } catch (error) {
                console.error('Error fetching article details:', error);
            }
        }

        setArticles(newArticles);
    };


    return (
        <div className="ArticleFetcher">
            <div className="control-panel">
                <input
                    type="range"
                    min="10"
                    max="600"
                    value={fetchInterval}
                    className="slider"
                    onChange={handleSliderChange}
                />
                <div>Fetch interval: {fetchInterval} seconds</div>
                <div>Time until next fetch: {timeLeft} seconds</div>
            </div>

            <div className="articles-container">
                {showNoArticlesMessage && (
                    <div className="message" style={{ opacity: messageOpacity }}>
                        No new articles were found.
                    </div>
                )}

                {Array.isArray(articles) && articles.length > 0 && (
                    <div className="articles-container">
                        {articles.map((article, index) => (
                            <div
                                key={index}
                                className={`article ${article.isNew ? 'article-new' : ''}`}
                            >
                                <div>Title: {decodeHtml(article.title)}</div>
                                <div>
                                    <span>Link: </span>
                                    <a href={article.link} className="custom-link">
                                        {article.link}
                                    </a>
                                </div>
                                <button onClick={() => handleArticleDetails(article.link, index)}>
                                    {article.detailsVisible ? 'Hide Details' : 'View Details'}
                                </button>
                                {article.detailsVisible && (
                                    <div className="article-details">
                                        <p>{article.content || 'Loading...'}</p>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default ArticleFetcher;
