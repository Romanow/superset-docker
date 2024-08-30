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
            void embedded("40eccf4f-56de-4bfc-9f34-a057a6ad39da")
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
