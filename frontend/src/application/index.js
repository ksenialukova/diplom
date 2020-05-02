import React, { Component } from 'react'
import axios from 'axios'

import DatePicker from 'react-datepicker'
import GoogleMapReact from 'google-map-react'

import 'react-datepicker/dist/react-datepicker.css'

const marker = (map, maps, entity) => {
    const marker = new maps.Marker({
        position: { lat: parseFloat(entity.lat), lng: parseFloat(entity.lng) },
        map: map,
        label: entity.type
    })
    const CashEntityCard = new maps.InfoWindow({
        content:
            `<div>
                <div>Type: ${entity.type}</div>
                <div>Lat: ${entity.lat} Lng: ${entity.lng}</div>
                <div>Address</div>
                <div>Last Shipment</div>
                <div>Next Shipment</div>
                <div>Intensity: ${entity.intensity}</div>
        </div>`
    })
    marker.addListener('click', () => {
        CashEntityCard.open(map, marker)
    })
}

const direction = (map, maps) => {
    const directionsDisplay = new maps.DirectionsRenderer()
    const directionsService = new maps.DirectionsService();
    const request = {
        origin: new maps.LatLng(50.4250244,30.4503335),
        destination: new maps.LatLng(50.4338805,30.4532582),
        waypoints: [
            {
                location: new maps.LatLng(50.4612044,30.4537611),
                stopover:true
            }
            ],
        travelMode: maps.DirectionsTravelMode.DRIVING
    }
    directionsService.route(request, function(response, status) {
        if (status === maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        }
    })
    directionsDisplay.setMap(map);
}


const setup = (map, maps, state) => {
    const directionsDisplay = new maps.DirectionsRenderer()
    const directionsService = new maps.DirectionsService()

    const waypoints = state.plan.map((entity) => {
        return {
            location: new maps.LatLng(entity.lat, entity.lng),
            stopover: true
        }
        })
    const request = {
        origin: new maps.LatLng(state.plan[0].lat, state.plan[0].lng),
        destination: new maps.LatLng(state.plan[0].lat, state.plan[0].lng),
        waypoints: waypoints,
        travelMode: maps.DirectionsTravelMode.DRIVING
    }
    directionsService.route(request, function(response, status) {
        if (status === maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        }
    })
    directionsDisplay.setMap(map);

    return state.cash_entities
        ? state.cash_entities.map((entity) => {
                marker(map, maps, entity)
            }
        )
        : 'Loading...'
}

class Application extends Component {
    constructor(props) {
        super(props)
        this.state = {
            date: new Date(2020, 2, 18),
            center: {
                lat: 50.4250244,
                lng: 30.4503335
            },
            zoom: 11,
            cash_entities: [],
            shipments: [],
            plan: []
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

    componentDidMount() {
        this.fetchAtms()
        this.fetchShipments()
        this.fetchPlan()
    }

    update() {
        this.fetchAtms()
        this.fetchPlan()
    }


    render() {
    return (
        <div>
          <div>
            <DatePicker
                selected={this.state.date}
                dateFormat="yyyy-MM-dd"
                onChange={(newValue) => this.setState({date: newValue}, () => this.update())}
            />
          </div>
            <div style={{ width: "75vw", height: "75vh" }}>
                <GoogleMapReact
                    bootstrapURLKeys={{ key: ''}}
                    defaultCenter={this.state.center}
                    defaultZoom={this.state.zoom}
                    onGoogleApiLoaded={({map, maps}) => setup(map, maps, this.state)}
                    yesIWantToUseGoogleMapApiInternals
                >
                </GoogleMapReact>
            </div>
            <div>
                <br/>
                Shipments
                {this.state.shipments
                        ? <ul>
                        <li>Date Length Cost</li>
                        {this.state.shipments.map((shipment) =>
                            <li key={shipment.cost+shipment.length}>
                                {shipment.date} {shipment.length} {shipment.cost}
                            </li>
                        )}</ul>
                        : 'Loading...'
                }
            </div>
            <div>
                <button onClick={this.handleClick}>
                    Run Analytics
                </button>
                <button onClick={this.handleClick}>
                    Report
                </button>
            </div>
        </div>
    )
  }
}

export default Application
