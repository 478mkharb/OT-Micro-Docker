import react, * as React from "react";
import { Page, Grid, Table } from "tabler-react";
import SiteWrapper from "./SiteWrapper.react";

class ListEmployee extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            data: []
        };
    }

    loadData() {
        fetch("/api/v1/employee/search/all")
            .then(response => response.json())
            .then(data => {

                const sortedData = Array.isArray(data)
                    ? data.sort((a, b) => Number(a.id) - Number(b.id))
                    : [];

                this.setState({
                    data: sortedData
                });

            })
            .catch(err => console.error(err.toString()));
    }

    componentDidMount() {
        this.loadData();
    }

    render() {
        return (
            <SiteWrapper>

                <Page.Card title="Employee List"></Page.Card>

                <Grid.Col md={6} lg={10} className="align-self-center">

                    <Table>

                        <Table.Header>
                            <Table.ColHeader>Employee ID</Table.ColHeader>
                            <Table.ColHeader>Name</Table.ColHeader>
                            <Table.ColHeader>Email</Table.ColHeader>
                            <Table.ColHeader>Phone Number</Table.ColHeader>
                            <Table.ColHeader>Job Role</Table.ColHeader>
                            <Table.ColHeader>Job Location</Table.ColHeader>
                        </Table.Header>

                        <Table.Body>

                            {
                                Array.isArray(this.state.data) &&
                                this.state.data.map((item) => {

                                    return (
                                        <Table.Row key={item.id}>

                                            <Table.Col>{item.id}</Table.Col>

                                            <Table.Col>
                                                {item.name}
                                            </Table.Col>

                                            <Table.Col>
                                                {item.email}
                                            </Table.Col>

                                            <Table.Col>
                                                {item.phone_number}
                                            </Table.Col>

                                            <Table.Col>
                                                {item.designation || "N/A"}
                                            </Table.Col>

                                            <Table.Col>
                                                {item.office_location || "N/A"}
                                            </Table.Col>

                                        </Table.Row>
                                    );
                                })
                            }

                        </Table.Body>

                    </Table>

                </Grid.Col>

            </SiteWrapper>
        );
    }
}

export default ListEmployee;
