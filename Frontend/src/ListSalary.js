import react, * as React from "react";
import { Page, Grid, Table, Button } from "tabler-react";
import SiteWrapper from "./SiteWrapper.react";
import jsPDF from "jspdf";
import "jspdf-autotable";

class ListSalary extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            data: []
        };
    }

    loadData() {

        fetch("/api/v1/salary/search/all")
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

    createPDF() {

        const doc = new jsPDF();

        doc.text("Salary Report", 14, 15);

        const tableColumn = [
            "Employee ID",
            "Name",
            "Salary Amount",
            "Status"
        ];

        const tableRows = [];

        this.state.data.forEach(item => {

            const rowData = [
                item.id,
                item.name,
                item.salary,
                item.status
            ];

            tableRows.push(rowData);
        });

        doc.autoTable({
            head: [tableColumn],
            body: tableRows,
            startY: 20
        });

        doc.save("salary-report.pdf");
    }

    render() {

        return (

            <SiteWrapper>

                <Page.Card title="Salary List"></Page.Card>

                <Grid.Col md={6} lg={10} className="align-self-center">

                    <Button
                        color="primary"
                        onClick={() => this.createPDF()}
                    >
                        Create PDF
                    </Button>

                    <br />
                    <br />

                    <Table>

                        <Table.Header>

                            <Table.ColHeader>
                                Employee ID
                            </Table.ColHeader>

                            <Table.ColHeader>
                                Name
                            </Table.ColHeader>

                            <Table.ColHeader>
                                Salary Amount
                            </Table.ColHeader>

                            <Table.ColHeader>
                                Status
                            </Table.ColHeader>

                        </Table.Header>

                        <Table.Body>

                            {
                                Array.isArray(this.state.data) &&
                                this.state.data.map((item) => {

                                    return (

                                        <Table.Row key={item.id}>

                                            <Table.Col>
                                                {item.id}
                                            </Table.Col>

                                            <Table.Col>
                                                {item.name}
                                            </Table.Col>

                                            <Table.Col>
                                                {item.salary}
                                            </Table.Col>

                                            <Table.Col>
                                                {item.status}
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

export default ListSalary;
