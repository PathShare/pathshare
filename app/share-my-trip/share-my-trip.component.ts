import { NgForm } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { ShareMyTripService } from './share-my-trip.service';



@Component({
  selector: 'app-share-my-trip',
  templateUrl: './share-my-trip.component.html',
  styleUrls: ['./share-my-trip.component.css']
})
export class ShareMyTripComponent implements OnInit {

  constructor(private shareMyTripService:ShareMyTripService) { }

  ngOnInit() {
  }

  today = new Date().toJSON().split('T')[0];

  onShare(form: NgForm) {
    const startingLocation = form.value.startingLocation;
    const destinationLocation = form.value.destinationLocation;
    const inputDate = form.value.inputDate;
    const numOfSeats = form.value.numOfSeats;
    const price = form.value.price;

    this.shareMyTripService.shareMyTrip(startingLocation,destinationLocation,inputDate,numOfSeats,price)
    
  }
}
