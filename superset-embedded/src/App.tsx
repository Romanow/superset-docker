import React, {FC, useEffect, useRef, useState} from "react";
import {embedDashboard} from "@superset-ui/embedded-sdk";
import {Api} from "./Api"
import "./App.css";

export const useSupersetEmbed = (dashboardId: string) => {
    const [mounted, setMounted] = useState(false);
    const ref = useRef(null);

    useEffect(() => {
        if (!ref.current) return;
        if (mounted) return;

        void embedDashboard({
            id: dashboardId,
            supersetDomain: "http://localhost:8088",
            mountPoint: ref.current as HTMLElement,
            fetchGuestToken: () => Api.token("program", "test", dashboardId),
            dashboardUiConfig: {
                hideTitle: true,
                hideChartControls: true,
                hideTab: true,
            },
        });

        setMounted(true);
    }, [dashboardId, mounted]);

    return ref;
};

const App: FC = () => {
    const embedded = useSupersetEmbed("40eccf4f-56de-4bfc-9f34-a057a6ad39da");
    return (
        <div className="container">
            <h1>Apache Superset Embedded Dashboard</h1>
            <div id="superset" ref={embedded}></div>
        </div>
    );
}

export default App;
