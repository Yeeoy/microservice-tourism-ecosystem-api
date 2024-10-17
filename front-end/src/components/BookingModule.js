import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { post } from '../utils/api';
import { toast } from 'react-toastify';

const BookingModule = ({ hotelId, roomTypes, isLoggedIn }) => {
  const { t } = useTranslation();
  const [checkInDate, setCheckInDate] = useState('');
  const [checkOutDate, setCheckOutDate] = useState('');
  const [selectedRoomType, setSelectedRoomType] = useState('');
  const [numberOfRooms, setNumberOfRooms] = useState(1);

  const handleBooking = async (e) => {
    e.preventDefault();
    if (!isLoggedIn) {
      toast.error(t('pleaseLoginToBook'));
      return;
    }
    try {
      const response = await post('/api/accommodation/room-booking/', {
        accommodation_id: hotelId,
        room_type_id: selectedRoomType,
        check_in_date: checkInDate,
        check_out_date: checkOutDate,
        number_of_rooms: numberOfRooms,
      });
      if (response.code === 201) {
        toast.success(t('bookingSuccessful'));
      } else {
        throw new Error(response.msg || t('bookingFailed'));
      }
    } catch (err) {
      toast.error(err.message || t('bookingFailed'));
    }
  };

  return (
    <div className="bg-white shadow-lg rounded-lg overflow-hidden mb-8">
      <div className="p-6">
        <h2 className="text-2xl font-bold mb-4">{t('bookYourStay')}</h2>
        <form onSubmit={handleBooking}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="checkInDate">
              {t('checkInDate')}
            </label>
            <input
              type="date"
              id="checkInDate"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={checkInDate}
              onChange={(e) => setCheckInDate(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="checkOutDate">
              {t('checkOutDate')}
            </label>
            <input
              type="date"
              id="checkOutDate"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={checkOutDate}
              onChange={(e) => setCheckOutDate(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="roomType">
              {t('roomType')}
            </label>
            <select
              id="roomType"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={selectedRoomType}
              onChange={(e) => setSelectedRoomType(e.target.value)}
              required
            >
              <option value="">{t('selectRoomType')}</option>
              {Object.entries(roomTypes).map(([id, type]) => (
                <option key={id} value={id}>{type.room_type}</option>
              ))}
            </select>
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="numberOfRooms">
              {t('numberOfRooms')}
            </label>
            <input
              type="number"
              id="numberOfRooms"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              value={numberOfRooms}
              onChange={(e) => setNumberOfRooms(parseInt(e.target.value))}
              min="1"
              required
            />
          </div>
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
          >
            {t('bookNow')}
          </button>
        </form>
      </div>
    </div>
  );
};

export default BookingModule;
