import react, * as React from "react";
import { Page, Grid } from "tabler-react";
import SiteWrapper from "./SiteWrapper.react";
import { Button, Form, FormGroup, Label, Input } from "reactstrap";
import { withFormik } from "formik";

const AttendanceForm = ({
  values,
  handleChange,
  handleSubmit,
  errors,
  touched,
  isSubmitting
}) => {
  return (
    <SiteWrapper>
      <Page.Card title="Log Attendance"></Page.Card>

      <Grid.Col md={6} lg={6} className="align-self-center">
        <Form onSubmit={handleSubmit}>

          <FormGroup>
            {touched.id && errors.id && (
              <p className="red">{errors.id}</p>
            )}

            <Label for="id">Employee ID</Label>

            <Input
              type="text"
              name="id"
              id="id"
              placeholder="Employee ID"
              value={values.id}
              onChange={handleChange}
            />
          </FormGroup>

          <FormGroup>
            {touched.name && errors.name && (
              <p className="red">{errors.name}</p>
            )}

            <Label for="name">Employee Name</Label>

            <Input
              type="text"
              name="name"
              id="name"
              placeholder="Employee Name"
              value={values.name}
              onChange={handleChange}
            />
          </FormGroup>

          <FormGroup>
            {touched.status && errors.status && (
              <p className="red">{errors.status}</p>
            )}

            <Label for="status">Status</Label>

            <Input
              type="select"
              name="status"
              id="status"
              value={values.status}
              onChange={handleChange}
            >
              <option value="">Select Status</option>
              <option value="Present">Present</option>
              <option value="Absent">Absent</option>
            </Input>
          </FormGroup>

          <FormGroup>
            {touched.date && errors.date && (
              <p className="red">{errors.date}</p>
            )}

            <Label for="date">Date</Label>

            <Input
              type="date"
              name="date"
              id="date"
              value={values.date}
              onChange={handleChange}
            />
          </FormGroup>

          <Button color="primary" disabled={isSubmitting}>
            Submit
          </Button>

        </Form>
      </Grid.Col>
    </SiteWrapper>
  );
};

const FormikApp = withFormik({

  mapPropsToValues() {
    return {
      id: "",
      name: "",
      status: "",
      date: ""
    };
  },

  handleSubmit(values, { resetForm, setSubmitting }) {

    console.log("Submitting Attendance:", values);

    fetch("/api/v1/attendance/create", {
      method: "POST",
      body: JSON.stringify(values),
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(async (res) => {

        if (!res.ok) {
          const text = await res.text();
          throw new Error(text);
        }

        const data = await res.json();

        console.log("Attendance Response:", data);

        alert("Attendance logged successfully!");

        resetForm();
      })
      .catch((err) => {

        console.error(err);

        alert("Server Error");
      })
      .finally(() => {

        setSubmitting(false);
      });
  }

})(AttendanceForm);

export default FormikApp;
