
import { createBrowserRouter } from "react-router";

import AppLayout from "./AppLayout";

import HomePage from "../pages/HomePage";
import SummarizerPage from "../pages/SummarizerPage";
import NotFoundPage from "../pages/NotFoundPage";

export const router = createBrowserRouter([
    {
        path: "/",
        Component: AppLayout,
        children: [
            {
                index: true,
                Component: HomePage,
            },
            {
                path: "summarizer",
                Component: SummarizerPage,
            },
            {
                path: "*",
                Component: NotFoundPage,
            },
        ],
    },
]);
