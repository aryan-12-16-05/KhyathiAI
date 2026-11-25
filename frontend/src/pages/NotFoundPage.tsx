import { Link } from "react-router";

function NotFoundPage() {
    return (
        <main>
            <section aria-labelledby="not-found-title">
                <h1 id="not-found-title">
                    404 - Page Not Found
                </h1>

                <p>
                    The page you are looking for does not exist
                    or may have been moved.
                </p>

                <Link to="/">
                    Return to Home
                </Link>
            </section>
        </main>
    );
}

export default NotFoundPage;