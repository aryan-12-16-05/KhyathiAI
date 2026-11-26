
import "./Footer.css";

function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="site-footer">
            <div className="site-footer__inner">
                <div className="site-footer__branding">
                    <h2 className="site-footer__brand-name">
                        KhyathiAI
                    </h2>

                    <p>
                        One workspace for a growing collection of
                        useful AI tools.
                    </p>
                </div>

                <p className="site-footer__copyright">
                    © {currentYear} KhyathiAI. All rights reserved.
                </p>
            </div>
        </footer>
    );
}

export default Footer;
