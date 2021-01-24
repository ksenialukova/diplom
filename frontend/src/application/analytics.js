import React, { Component, Fragment } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'

import "./styles.css"

import Graph1 from './graph1'
import Graph2 from './graph2'

class Reports extends Component {

    constructor(props) {
        super(props)
        this.state = {
            graph1: [],
            graph2: []
        }
    }

    fetchData1 = async () => {
        const res = await axios.get('http://127.0.0.1:5002/graph1',
            {
                method: 'GET',
                mode: 'no-cors',
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    'Content-type': 'application/json'
                }
            }
        )
        console.log(res)
        this.setState({graph1: res.data.graph1})
        console.log(this.state)
  }
  fetchData2 = async () => {
        const res = await axios.get('http://127.0.0.1:5002/graph2',
            {
                method: 'GET',
                mode: 'no-cors',
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    'Content-type': 'application/json'
                }
            }
        )
        console.log(res)
        this.setState({graph2: res.data.graph2})
        console.log(this.state)
  }
  componentDidMount() {
    this.fetchData1()
    this.fetchData2()
  }

    render() {
    return (
        <Fragment>
            <div
                style={{
                    background: "#0e6655",
                    color: "#f7f9f9",
                    height: "9vh",
                    fontFamily: "Arial Black",
                    fontSize: "5vh",
                    paddingTop: "1vh",
                    paddingLeft: "2vh"
                }}
            >
                Bank Analytics
                <Link to='/'>
                    <button
                        style={{
                            width: "10vw",
                            height: "4vh",
                            color: "#0e6655",
                            background: "#f7f9f9",
                            border: "none",
                            borderRadius: "0.2rem",
                            fontFamily: "Arial Black",
                            fontSize: "1vw",
                            marginLeft: "65vw"
                        }}
                        onClick={this.handleClick}>
                        Main Page
                    </button>
                </Link>
            </div>

            <div>
                <div style={{ width: "40vw", height: "30vh", margin:"5vh", display: "inline-block"}}>
                    <Graph1 graph1={this.state.graph1}/>
                </div>
                <div style={{ width: "40vw", height: "30vh", margin:"5vh", display: "inline-block"}}>
                    <Graph2 graph2={this.state.graph2}/>
                </div>
            </div>
        </Fragment>
    )
  }
}

export default Reports
