
import { useNavigate } from "react-router";

import { Button } from "../../../components/ui";

import "./HeroSection.css";

function HeroSection() {
    const navigate = useNavigate();

    const handleExplore = () => {
        navigate("/summarizer");
    };

    return (
        <section
            className="hero-section"
            aria-labelledby="hero-title"
        >
            <div className="hero-section__content">

                <p className="hero-section__eyebrow">
                    YOUR AI-POWERED WORKSPACE
                </p>

                <h1
                    id="hero-title"
                    className="hero-section__title"
                >
                    One workspace.
                    <span> Many possibilities.</span>
                </h1>

                <p className="hero-section__description">
                    Welcome to KhyathiAI, a growing platform bringing
                    multiple intelligent tools together to simplify
                    everyday tasks and enhance productivity.
                </p>

                <p className="hero-section__supporting-text">
                    Start with our first feature: YouTube video summarization.
                    More possibilities are on the way.
                </p>

                <div className="hero-section__actions">
                    <Button
                        variant="primary"
                        size="large"
                        onClick={handleExplore}
                    >
                        Explore YouTube Summarizer
                    </Button>
                </div>

                <div className="hero-section__note">
                    <span
                        className="hero-section__note-dot"
                        aria-hidden="true"
                    />

                    Built to grow with your needs
                </div>

            </div>

            <div
                className="hero-section__visual"
                aria-hidden="true"
            >
                <div className="hero-visual__glow" />

                <div className="hero-visual__window">

                    <div className="hero-visual__topbar">
                        <div className="hero-visual__dots">
                            <span />
                            <span />
                            <span />
                        </div>

                        <span>KhyathiAI Workspace</span>
                    </div>

                    <div className="hero-visual__body">

                        <div className="hero-visual__welcome">
                            <span>YOUR AI WORKSPACE</span>
                            <h2>Explore possibilities.</h2>
                            <p>
                                Intelligent tools, one place.
                            </p>
                        </div>

                        <div className="hero-visual__feature">
                            <div className="hero-visual__feature-icon">
                                YT
                            </div>

                            <div className="hero-visual__feature-info">
                                <strong>YouTube Summarizer</strong>
                                <span>Our first feature</span>
                            </div>
                        </div>

                        <div className="hero-visual__upcoming">
                            <span className="hero-visual__plus">+</span>

                            <div>
                                <strong>More possibilities</strong>
                                <span>Coming as we grow</span>
                            </div>
                        </div>

                    </div>
                </div>
            </div>

        </section>
    );
}

export default HeroSection;
