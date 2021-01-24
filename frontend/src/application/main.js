import React, { Component, Fragment } from 'react'
import { withStyles } from '@material-ui/core/styles';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import axios from 'axios'
import moment from "moment"
import { Link } from 'react-router-dom'

import DatePicker from 'react-datepicker'

import 'react-datepicker/dist/react-datepicker.css'

import ShipmentsTable from './table'
import Map from '../icons/Screenshot 2020-12-09 at 22.44.38.png'

import "./styles.css"

const GreenCheckbox = withStyles({
  root: {
    color: "#0e6655",
    '&$checked': {
      color: "#0e6655",
    },
  },
  checked: {},
})((props) => <Checkbox color="default" {...props} />);

class Main extends Component {

    constructor(props) {
        super(props)
        this.state = {
            date: new Date(),
            center: {
                lat: 50.4250244,
                lng: 30.4503335
            },
            zoom: 11,
            cash_entities: [],
            shipments: [{
              date: '2020-12-10',
              length: 'BeerPoint',
              cost: '95%',
            }],
            plan: [],
            checkbox: false,
            files: []
        }
    }

    fetchAtms = async () => {
        const res = await axios.get('http://127.0.0.1:5002/intensity',
            {
                method: 'GET',
                mode: 'no-cors',
                params: {
                    date: this.state.date
                },
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    'Content-type': 'application/json'
                }
            }
        )
        this.setState({cash_entities: res.data.cash_entities})
    }

    fetchShipments = async () => {
        const res = await axios.get('http://127.0.0.1:5002/shipments',
            {
                method: 'GET',
                mode: 'no-cors',
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    'Content-type': 'application/json'
                }
            }
        )
        this.setState({shipments: res.data.shipments})
    }

    fetchPlan = async () => {
        const res = await axios.get('http://127.0.0.1:5002/plan_by_date',
            {
                method: 'GET',
                mode: 'no-cors',
                params: {
                    date: this.state.date
                },
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    'Content-type': 'application/json'
                }
            }
        )
        this.setState({plan: res.data.plan})
        console.log(this.state)
    }

    runAnalytics = async () => {
        const res = await axios.get('http://127.0.0.1:5002/run_analytics',
            {
                method: 'GET',
                mode: 'no-cors',
                params: {
                    date: this.state.date
                },
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    'Content-type': 'application/json'
                }
            }
        )
        this.setState({plan: res.data.plan})
        console.log(this.state)
    }

    componentDidMount() {
        this.fetchAtms()
        // this.fetchShipments()
        this.fetchPlan()
    }

    update() {
        console.log(this.state.date)
        this.fetchAtms()
        this.fetchPlan()
    }

    handleDatePickerClick(date) {
        this.setState({date: new Date(date)}, ()=>this.update())
    }

    render() {
    return (
        <Fragment>
            <div
                style={{
                    background: "#000000",
                    color: "#f7f9f9",
                    height: "9vh",
                    fontFamily: "Arial Black",
                    fontSize: "5vh",
                    paddingTop: "1vh",
                    paddingLeft: "2vh",
                    textAlign: "center"
                }}
            >
                BeerLog
            </div>

            <div style={{ width: "50vw", height: "75vh", display: "inline-block", marginTop: "2.5vh", marginRight: "2.5vh", marginLeft: "2.5vh"}}>
              <img src={Map} />
            </div>

            <div style={{display: "inline-block"}}>
                <div style={{display: "inline-block"}}>
                    <DatePicker
                        inline
                        selected={this.state.date}
                        onChange={(date) => this.handleDatePickerClick(date)}
                        maxDate={new Date(new Date().getFullYear(),new Date().getMonth(),new Date().getDate()+5)}
                    />
                </div>
                {this.state.shipments
                &&
                <div style={{ width: "40vw", height: "100vh", margin: "2.5vh" }}>
                    <ShipmentsTable rows={this.state.shipments}/>
                </div>}
            </div>

        </Fragment>
    )
  }
}

export default Main
