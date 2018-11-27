import { Component, OnInit } from '@angular/core';
import { SearchFormService } from '../shared/services/search-form.service';
import { SearchService } from '../trip-search/search.service';
import { Ride } from '../shared/model/ride';
import { FormGroup, FormControl, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-ride-listings',
  templateUrl: './ride-listings.component.html',
  styleUrls: ['./ride-listings.component.css']
})
export class RideListingsComponent implements OnInit {

  parameters: any;

  // Keep a publicly-exposed result list responsive to sort actions.
  private rides: Ride[];
  sortedRides: Ride[];

  sortForm = new FormGroup({
    priceSort: new FormControl()
  });

  constructor(
    private formService: SearchFormService,
    private searchService: SearchService,
    private builder: FormBuilder) { }

  ngOnInit() {
    this.sortForm = this.builder.group({
      priceSort: ['']
    });

    this.rides = [];
    this.sortedRides = [];

    // Get search results based on parameters passed from form
    this.parameters = this.formService.getSearchQuery();
    this.searchService.getRides(this.parameters['start'], this.parameters['end'],
    this.parameters['date']).subscribe(rides => {
      this.rides = rides;
      this.sortedRides = rides;
    });
  }

  public getFormattedDate(date: string) {
    const formattedDate = new Date(`${date}T00:00:00`).toDateString();
    if (formattedDate === 'Invalid Date') {
      return '';
    }
    return formattedDate;
  }

  public onPriceSort() {
    switch (this.sortForm.controls['priceSort'].value) {
      case 0:
        // Reset sorted list to original
        this.sortedRides = this.rides;
        break;
      case 1:
        // Sort low to high
        let temp = [];
        temp = this.rides.sort((left, right): number => {
          if (left.seatPrice < right.seatPrice) {return -1; }
          if (left.seatPrice > right.seatPrice) {return 1; }
          return 0;
        });
        this.sortedRides = [];
        temp.forEach(ride => {
          this.sortedRides.push(ride);
        });
        break;
      case 2:
        // Sort high to low
        let tempRides = [];
        tempRides = this.rides.sort((left, right): number => {
          if (left.seatPrice < right.seatPrice) {return 1; }
          if (left.seatPrice > right.seatPrice) {return -1; }
          return 0;
        });
        this.sortedRides = [];
        tempRides.forEach(ride => {
          this.sortedRides.push(ride);
        });
        break;
      default:
        break;
    }
  }
}
