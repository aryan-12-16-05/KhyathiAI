
import { useState } from "react";
import { Link, NavLink } from "react-router";

import "./Header.css";

function Header() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const closeMenu = () => {
        setIsMenuOpen(false);
    };

    return (
        <header className="site-header">
            <div className="site-header__inner">

                {/* Brand */}
                <Link
                    to="/"
                    className="site-header__brand"
                    aria-label="KhyathiAI home"
                    onClick={closeMenu}
                >
                    <span className="site-header__brand-mark" aria-hidden="true">
                        K
                    </span>

                    <span className="site-header__brand-name">
                        KhyathiAI
                    </span>
                </Link>

                {/* Mobile menu button */}
                <button
                    type="button"
                    className="site-header__menu-toggle"
                    aria-label={
                        isMenuOpen
                            ? "Close navigation menu"
                            : "Open navigation menu"
                    }
                    aria-expanded={isMenuOpen}
                    aria-controls="primary-navigation"
                    onClick={() => setIsMenuOpen((previous) => !previous)}
                >
                    <span />
                    <span />
                    <span />
                </button>

                {/* Navigation */}
                <nav
                    id="primary-navigation"
                    className={`site-header__navigation ${isMenuOpen ? "is-open" : ""
                        }`}
                    aria-label="Primary navigation"
                >
                    <NavLink
                        to="/"
                        end
                        className={({ isActive }) =>
                            `site-header__link ${isActive ? "is-active" : ""}`
                        }
                        onClick={closeMenu}
                    >
                        Home
                    </NavLink>

                    <NavLink
                        to="/summarizer"
                        className={({ isActive }) =>
                            `site-header__link ${isActive ? "is-active" : ""}`
                        }
                        onClick={closeMenu}
                    >
                        YouTube Summarizer
                    </NavLink>
                </nav>

            </div>
        </header>
    );
}

export default Header;
