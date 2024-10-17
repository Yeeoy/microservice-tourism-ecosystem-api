import React from 'react';
import { Link } from 'react-router-dom';
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from 'react-icons/fa';
import { useTranslation } from 'react-i18next';

const Footer = () => {
    const { t } = useTranslation();

    return (
        <footer className="bg-gray-800 text-white py-12">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                    <div>
                        <h3 className="text-xl font-bold mb-4">{t('aboutTravely')}</h3>
                        <p className="text-gray-400">
                            {t('travelyDescription')}
                        </p>
                    </div>
                    <div>
                        <h3 className="text-xl font-bold mb-4">{t('quickLinks')}</h3>
                        <ul className="space-y-2">
                            <li><Link to="/" className="text-gray-400 hover:text-white">{t('home')}</Link></li>
                            <li><Link to="/hotels" className="text-gray-400 hover:text-white">{t('hotels')}</Link></li>
                            <li><Link to="/restaurants" className="text-gray-400 hover:text-white">{t('restaurants')}</Link></li>
                            <li><Link to="/events" className="text-gray-400 hover:text-white">{t('events')}</Link></li>
                            <li><Link to="/tours" className="text-gray-400 hover:text-white">{t('tours')}</Link></li>
                            <li><Link to="/transportation" className="text-gray-400 hover:text-white">{t('transportation')}</Link></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-xl font-bold mb-4">{t('contactUs')}</h3>
                        <p className="text-gray-400">{t('address')}: {t('companyAddress')}</p>
                        <p className="text-gray-400">{t('phone')}: {t('companyPhone')}</p>
                        <p className="text-gray-400">{t('email')}: {t('companyEmail')}</p>
                    </div>
                    <div>
                        <h3 className="text-xl font-bold mb-4">{t('followUs')}</h3>
                        <div className="flex space-x-4">
                            <a href="#" className="text-gray-400 hover:text-white"><FaFacebook size={24} /></a>
                            <a href="#" className="text-gray-400 hover:text-white"><FaTwitter size={24} /></a>
                            <a href="#" className="text-gray-400 hover:text-white"><FaInstagram size={24} /></a>
                            <a href="#" className="text-gray-400 hover:text-white"><FaLinkedin size={24} /></a>
                        </div>
                    </div>
                </div>
                <div className="mt-8 pt-8 border-t border-gray-700 text-center">
                    <p className="text-gray-400">&copy; 2023 Travely. {t('allRightsReserved')}</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
