import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RideListingsComponent } from './ride-listings.component';

describe('RideListingsComponent', () => {
  let component: RideListingsComponent;
  let fixture: ComponentFixture<RideListingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RideListingsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RideListingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
