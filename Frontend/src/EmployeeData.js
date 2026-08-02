import React, { useState, useEffect } from 'react';
import { Grid, StatsCard, Card } from 'tabler-react';
import C3Chart from "react-c3js";

const fetchAll = () =>
    fetch('/api/v1/employee/search/all').then(r => {
        if (!r.ok) throw new Error("Network issue");
        return r.json();
    });

function donutChart(data, colorMap) {
    return (
        <C3Chart
            style={{ height: "12rem" }}
            data={{
                columns: data,
                type: "donut",
                colors: colorMap
            }}
            donut={{
                title: ""
            }}
        />
    );
}

export const ListAllEmployees = () => {
    const [count, setCount] = useState(0);

    useEffect(() => {
        fetchAll()
            .then(data => setCount(data ? data.length : 0))
            .catch(() => setCount(0));
    }, []);

    return (
        <Grid.Col sm={3}>
            <StatsCard
                layout={1}
                movement={0}
                total={count}
                label="Total Employees"
            />
        </Grid.Col>
    );
};

export const ListEmployeeActiveEmployee = () => {
    const [count, setCount] = useState(0);

    useEffect(() => {
        fetchAll()
            .then(data => {
                setCount(
                    (data || []).filter(
                        e => e.status === "Current Employee"
                    ).length
                );
            })
            .catch(() => setCount(0));
    }, []);

    return (
        <Grid.Col sm={3}>
            <StatsCard
                layout={1}
                movement={0}
                total={count}
                label="Active Employees"
            />
        </Grid.Col>
    );
};

export const ListEmployeeInActiveEmployee = () => {
    const [count, setCount] = useState(0);

    useEffect(() => {
        fetchAll()
            .then(data => {
                setCount(
                    (data || []).filter(
                        e => e.status === "Ex-Employee"
                    ).length
                );
            })
            .catch(() => setCount(0));
    }, []);

    return (
        <Grid.Col sm={3}>
            <StatsCard
                layout={1}
                movement={0}
                total={count}
                label="Ex-Employees"
            />
        </Grid.Col>
    );
};

export const RoleDistribution = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetchAll()
            .then(res => {
                const devops = (res || []).filter(
                    e => (e.designation || "").includes("DevOps")
                ).length;

                const developer = (res || []).filter(
                    e => (e.designation || "").includes("Developer")
                ).length;

                if (devops > 0 || developer > 0) {
                    setData([
                        ["DevOps", devops],
                        ["Developer", developer]
                    ]);
                }
            })
            .catch(() => setData([]));
    }, []);

    return (
        <Grid.Col sm={4}>
            <Card>
                <Card.Header>
                    <Card.Title>Job Role Distribution</Card.Title>
                </Card.Header>

                <Card.Body>
                    {
                        data.length > 0
                            ? donutChart(data, {
                                DevOps: "#2563eb",
                                Developer: "#f97316"
                            })
                            : "Loading charts..."
                    }
                </Card.Body>
            </Card>
        </Grid.Col>
    );
};

export const LocationDistribution = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetchAll()
            .then(res => {

                const delhi = (res || []).filter(
                    e => (e.office_location || "").includes("Delhi")
                ).length;

                const bangalore = (res || []).filter(
                    e => (e.office_location || "").includes("Bangalore")
                ).length;

                const hyderabad = (res || []).filter(
                    e => (e.office_location || "").includes("Hyderabad")
                ).length;

                const noida = (res || []).filter(
                    e => (e.office_location || "").includes("Noida")
                ).length;

                if (
                    delhi > 0 ||
                    bangalore > 0 ||
                    hyderabad > 0 ||
                    noida > 0
                ) {
                    setData([
                        ["Delhi", delhi],
                        ["Bangalore", bangalore],
                        ["Hyderabad", hyderabad],
                        ["Noida", noida]
                    ]);
                }
            })
            .catch(() => setData([]));
    }, []);

    return (
        <Grid.Col sm={4}>
            <Card>
                <Card.Header>
                    <Card.Title>Locations Distribution</Card.Title>
                </Card.Header>

                <Card.Body>
                    {
                        data.length > 0
                            ? donutChart(data, {
                                Delhi: "#9333ea",
                                Bangalore: "#06b6d4",
                                Hyderabad: "#f97316",
                                Noida: "#22c55e"
                            })
                            : "Loading charts..."
                    }
                </Card.Body>
            </Card>
        </Grid.Col>
    );
};

export const StatusDistribution = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetchAll()
            .then(res => {

                const current = (res || []).filter(
                    e => e.status === "Current Employee"
                ).length;

                const ex = (res || []).filter(
                    e => e.status === "Ex-Employee"
                ).length;

                if (current > 0 || ex > 0) {
                    setData([
                        ["Current", current],
                        ["Ex", ex]
                    ]);
                }
            })
            .catch(() => setData([]));
    }, []);

    return (
        <Grid.Col sm={4}>
            <Card>
                <Card.Header>
                    <Card.Title>Employee Status Distribution</Card.Title>
                </Card.Header>

                <Card.Body>
                    {
                        data.length > 0
                            ? donutChart(data, {
                                Current: "#16a34a",
                                Ex: "#dc2626"
                            })
                            : "Loading charts..."
                    }
                </Card.Body>
            </Card>
        </Grid.Col>
    );
};
