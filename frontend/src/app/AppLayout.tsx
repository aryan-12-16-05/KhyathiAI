
import { Outlet } from "react-router";

import Header from "../components/layout/Header";
import Footer from "../components/layout/Footer";

import "./AppLayout.css";

function AppLayout() {
    return (
        <div className="app-layout">
            <Header />

            <div className="app-layout__content">
                <Outlet />
            </div>

            <Footer />
        </div>
    );
}

export default AppLayout;
