import React from 'react'
import { compose, withProps, lifecycle } from "recompose"
import { withScriptjs, withGoogleMap, GoogleMap, Marker, DirectionsRenderer, InfoWindow } from 'react-google-maps'

const google = window.google

class MarkerWithInfoWindow extends React.Component {

    constructor() {
        super();
        this.state = {
            isOpen: false
        }
        this.onToggleOpen = this.onToggleOpen.bind(this);
    }

    onToggleOpen() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    render() {
        return (
            <Marker
                position={this.props.position}
                onClick={this.onToggleOpen}
                icon={
                    this.props.type === 'A'
                        ? {url: require('./../icons/atm.png'),
                            scaledSize: {width: 32, height: 32}
                        }
                        : {url: require('./../icons/bank.png'),
                            scaledSize: {width: 32, height: 32}
                        }
                }
            >
            {
              this.state.isOpen && <InfoWindow onCloseClick={this.onToggleOpen}>
                <div>
                  <h3>Type: {this.props.type}</h3>
                  <h3>Lat: {this.props.lat} Lng: {this.props.lng}</h3>
                  <h3>Intensity: {this.props.intensity}</h3>
                </div>
            </InfoWindow>
            }
        </Marker>)
    }
}


const MapWithADirectionsRenderer = compose(
  withProps({
    googleMapURL: "https://maps.googleapis.com/maps/api/js?key=AIzaSyAjJiOQYpv9x7CWjzfcHFkRPmMJBTy_3C0&v=3.exp&libraries=geometry,drawing,places",
    loadingElement: <div style={{ height: `100%` }} />,
    containerElement: <div style={{ height: `400px` }} />,
    mapElement: <div style={{ width: "50vw", height: "75vh"}} />,
  }),
  withScriptjs,
  withGoogleMap,
  lifecycle({
    componentDidMount() {
        if (this.props.plan.length) {
          const DirectionsService = new google.maps.DirectionsService()

          const waypoints = this.props.plan.map((entity) => {
                  return {
                      location: new google.maps.LatLng(entity.lat, entity.lng),
                      stopover: true
                  }
              })

            DirectionsService.route({
              origin: new google.maps.LatLng(this.props.plan[0].lat, this.props.plan[0].lng),
              destination: new google.maps.LatLng(this.props.plan[0].lat, this.props.plan[0].lng),
              waypoints: waypoints,
            travelMode: google.maps.TravelMode.DRIVING,
          }, (result, status) => {
            if (status === google.maps.DirectionsStatus.OK) {
              this.setState({
                directions: result,
              });
            } else {
              console.error(`error fetching directions ${result}`);
            }
          })
        }
        },
    componentWillReceiveProps() {
      if (this.props.plan.length) {
        const DirectionsService = new google.maps.DirectionsService()

        const waypoints = this.props.plan.slice(1, this.props.plan.length-1).map((entity) => {
          return {
            location: new google.maps.LatLng(entity.lat, entity.lng),
            stopover: true
          }
        })

        DirectionsService.route({
          origin: new google.maps.LatLng(this.props.plan[0].lat, this.props.plan[0].lng),
          destination: new google.maps.LatLng(this.props.plan[this.props.plan.length-1].lat, this.props.plan[this.props.plan.length-1].lng),
          waypoints: waypoints,
          travelMode: google.maps.TravelMode.DRIVING,
        }, (result, status) => {
          if (status === google.maps.DirectionsStatus.OK) {
            this.setState({
              directions: result,
            });
          } else {
            console.error(`error fetching directions ${result}`);
          }
        })
      } else {
        this.setState({
              directions: null,
            });
      }
    }
  })
)(props =>
  <GoogleMap
    defaultZoom={12}
    defaultCenter={new google.maps.LatLng(50.425307, 30.459151)}
  >
    {
      props.cash_entities.map((entity) => {
        return <MarkerWithInfoWindow
            position={{ lat: parseFloat(entity.lat), lng:parseFloat(entity.lng) }}
            type={entity.type}
            intensity={entity.intensity}
            lat={entity.lat}
            lng={entity.lng}
        />
      })
    }
    {props.directions && <DirectionsRenderer directions={props.directions} />}
  </GoogleMap>
)

export default MapWithADirectionsRenderer
