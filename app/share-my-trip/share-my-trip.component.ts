import { NgForm } from '@angular/forms';
import { Component, OnInit } from '@angular/core';



@Component({
  selector: 'app-share-my-trip',
  templateUrl: './share-my-trip.component.html',
  styleUrls: ['./share-my-trip.component.css']
})
export class ShareMyTripComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  onSignup(form: NgForm) {
    const startingLocation = form.value.startingLocation;
    const destinationLocation = form.value.destinationLocation;
    const inputDate = form.value.inputDate;
    const numOfSeats = form.value.numOfSeats;
    const price = form.value.price;

    // this.authService.signupUser(name,major,age,username,email,password); something like this for sharetripservice?
  }

}
