import React, {FC, useEffect} from "react";
import {embedDashboard} from "@superset-ui/embedded-sdk";
import {Api} from "./Api"
import "./App.css";

const App: FC = () => {
    useEffect(() => {
        const embedded = async (dashboardId: string) => {
            await embedDashboard({
                id: dashboardId,
                supersetDomain: "http://localhost:8088",
                mountPoint: document.getElementById("superset") as HTMLElement,
                fetchGuestToken: () => Api.token("program", "test", dashboardId),
                dashboardUiConfig: {
                    hideTitle: true,
                    hideChartControls: true,
                    hideTab: true,
                },
            });
        }
        if (document.getElementById("superset")) {
            void embedded("6faa5694-4837-477f-8065-57b50ed36cb4") // embedded dashboard ID
        }
    }, []);

    return (
        <div className="container">
            <h1>Apache Superset Embedded Dashboard</h1>
            <div id="superset"></div>
        </div>
    );
}

export default App;
