import React, { Component } from "react";
import { Datatable } from "@o2xp/react-datatable";
import { chunk } from "lodash";
import axios from "axios";

const options = {
  title: "Fullness",
  dimensions: {
    datatable: {
      width: "100%",
      height: "45%"
    },
    row: {
      height: "48px"
    }
  },
  keyColumn: "id",
  font: "Arial",
  data: {
    columns: [
      {
        id: "date",
        label: "Date",
        colSize: "50px"
      },
      {
        id: "length",
        label: "Point",
        colSize: "40px",
      },
      {
        id: "cost",
        label: "Fullness",
        colSize: "40px",
      }
    ],
    rows: []
  },
  features: {
    canDelete: true,
  }
};

class App extends Component {
  constructor(props) {
    super(props)
  }
  actionsRow = async ({ payload }) => {
    console.log(payload);
    console.log(payload.date);
    const { date } = payload
    const { type } = payload
    const res = await axios.get('http://127.0.0.1:5002/delete_shipment',
            {
                method: 'GET',
                mode: 'no-cors',
                params: {
                    date,
                    type
                },
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    'Content-type': 'application/json'
                }
            }
        )
    console.log(res)
  };

  refreshRows = () => {
    const { rows } = this.props;
    const randomRows = Math.floor(Math.random() * rows.length) + 1;
    const randomTime = Math.floor(Math.random() * 4000) + 1000;
    const randomResolve = Math.floor(Math.random() * 10) + 1;
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (randomResolve > 3) {
          resolve(chunk(rows, randomRows)[0]);
        }
        reject(new Error("err"));
      }, randomTime);
    });
  };

  render() {
    const { rows } = this.props;
    options.data.rows = rows
    return (
      <Datatable
        options={options}
        refreshRows={this.refreshRows}
        actions={this.actionsRow}
      />
    );
  }
}

export default App;
