import react, * as React from "react";
import { Page, Grid, Table } from "tabler-react";
import SiteWrapper from "./SiteWrapper.react";

class ListEmployee extends React.Component {
        constructor(props) {
                super(props)
                this.state = { data: [] }
        }

        loadData() {
                fetch('/api/v1/attendance/search/all')
                        .then(response => {
                            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
                            return response.json();
                        })
                        .then(data => {
                                this.setState({data: Array.isArray(data) ? data : [] })
                })
                        .catch(err => console.error(err.toString()))
        }

        componentDidMount() {
                this.loadData()
        }

  render() {
      return (
          <SiteWrapper>
          <Page.Card title="Attendance List"></Page.Card>
          <Grid.Col md={6} lg={10} className="align-self-center">
          <Table>
            <Table.Header>
                 <Table.ColHeader>Employee ID</Table.ColHeader>
                 <Table.ColHeader>Status</Table.ColHeader>
                 <Table.ColHeader>Date</Table.ColHeader>
            </Table.Header>
            <Table.Body>
           { Array.isArray(this.state.data) && this.state.data.map((item, i) => {
                return (
                    <Table.Row key={i}>
                        <Table.Col>{item.id}</Table.Col>
                        <Table.Col>{item.status}</Table.Col>
                        <Table.Col>{item.date}</Table.Col>
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
