import { Component, OnInit } from '@angular/core';
import { Ride, Coordinate } from '../shared/model/ride';
import { SearchService } from './search.service';

interface Segment {start: Coordinate; end: Coordinate; }

@Component({
  selector: 'app-trip-search',
  templateUrl: './trip-search.component.html',
  styleUrls: ['./trip-search.component.css']
})
export class TripSearchComponent implements OnInit {

  // Stores scaled Cartesian coordinates to plot on map.
  allTripPoints: Coordinate[];

  // Stores segments between start and end points to plot on map.
  allTripSegments: Segment[];

  constructor(private searchService: SearchService) { }

  ngOnInit() {
    this.allTripPoints = [];
    this.allTripSegments = [];

    this.searchService.getAllRides().subscribe(rides => {
      rides.forEach(ride => {
        this.allTripPoints.push(ride.departureLocation);
        this.allTripPoints.push(ride.destinationLocation);
        this.allTripSegments.push({start: ride.departureLocation, end: ride.destinationLocation});
      });
    });
  }

  /**
   * @description projects the geographic coordinates of a ride to the map
   * displayed on the main page.
   * @param latitude WGS84 format
   * @param longitude WGS84 format
   */
  private coordinateToPosition(latitude: number, longitude: number) {
    const LEFT_MARGIN = 285;
    const RIGHT_MARGIN = 810;
    const TOP_MARGIN = 0;
    const BOTTOM_MARGIN = 325;

    const LEFT_LONGITUDE = -124.271;
    const RIGHT_LONGITUDE = -66.897;
    const TOP_LATITUDE = 48.969;
    const BOTTOM_LATITUDE = 25.257;

    // How far between our lat/long margins the point lies
    const latMargin = ((latitude - BOTTOM_LATITUDE) / (TOP_LATITUDE - BOTTOM_LATITUDE));
    const longMargin = ((longitude - LEFT_LONGITUDE) / (RIGHT_LONGITUDE - LEFT_LONGITUDE));

    return {x: LEFT_MARGIN + ((RIGHT_MARGIN - LEFT_MARGIN) * latMargin),
            y: BOTTOM_MARGIN - ((BOTTOM_MARGIN - TOP_MARGIN) * longMargin)};
  }

  private getTripPath(segment: Segment) {
    const startPosition = this.coordinateToPosition(segment.start.latitude, segment.start.longitude);
    const endPosition = this.coordinateToPosition(segment.end.latitude, segment.end.longitude);
    return `m50 50 100 100`;
  }
}
