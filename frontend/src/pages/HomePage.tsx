import { Link } from "react-router";

function HomePage() {
    return (
        <main>
            <section aria-labelledby="home-title">
                <p>YOUR AI-POWERED WORKSPACE</p>

                <h1 id="home-title">Welcome to KhyathiAI</h1>

                <p>
                    A growing collection of intelligent tools designed
                    to make everyday tasks easier and more productive.
                </p>

                <Link to="/summarizer">
                    Explore our first feature
                </Link>
            </section>
        </main>
    );
}

export default HomePage;

