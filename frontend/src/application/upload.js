import React, { Component, Fragment } from 'react'
import Dropzone from 'react-dropzone'
import { Link } from 'react-router-dom'


import "./styles.css"
import axios from "axios";

class Upload extends Component {

    constructor(props) {
        super(props)
        this.state = {
            files: []
        }
    }

    handleDrop = async (acceptedFiles) => {
        this.setState({files: acceptedFiles})
        const res = await axios.get('http://127.0.0.1:5002/upload',
            {
                method: 'POST',
                mode: 'no-cors',
                body: acceptedFiles,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    'Content-type': 'csv'
                }
            }
        )
        console.log(this.state)
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
                <Dropzone onDrop={this.handleDrop}>
                    {({ getRootProps, getInputProps }) => (
                        <div {...getRootProps({ className: "dropzone" })}>
                            <input {...getInputProps()} />
                            <p>Drag'n'drop files, or click to select files</p>
                        </div>
                    )}
                </Dropzone>
                <div>
                    <strong>Files:</strong>
                    {<ul>
                        {this.state.files.map((file) => <li key={file.name}>{file.name}</li>)}
                    </ul>}
                </div>
            </div>



        </Fragment>
    )
  }
}

export default Upload
