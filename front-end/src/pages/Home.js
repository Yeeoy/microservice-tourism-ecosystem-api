import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { get } from "../utils/api";
import { toast } from "react-toastify";
import { useTranslation } from 'react-i18next';
import {
    CalendarIcon,
    ClockIcon,
    MapPinIcon,
    UserGroupIcon,
    CurrencyDollarIcon,
    TicketIcon,
    TagIcon,
    ChevronLeftIcon,
    ChevronRightIcon,
    GlobeAltIcon,
    BoltIcon,
    SparklesIcon,
    StarIcon,
    HomeIcon,
    PhoneIcon
} from "@heroicons/react/24/solid";

const Home = () => {
    const { t } = useTranslation();
    const [featuredItems, setFeaturedItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showLeftButton, setShowLeftButton] = useState(false);
    const [showRightButton, setShowRightButton] = useState(true);
    const featuredContainerRef = useRef(null);

    useEffect(() => {
        fetchFeaturedItems();
    }, []);

    useEffect(() => {
        const checkScrollButtons = () => {
            if (featuredContainerRef.current) {
                const { scrollLeft, scrollWidth, clientWidth } = featuredContainerRef.current;
                setShowLeftButton(scrollLeft > 0);
                setShowRightButton(scrollLeft < scrollWidth - clientWidth);
            }
        };

        checkScrollButtons();
        window.addEventListener('resize', checkScrollButtons);

        return () => window.removeEventListener('resize', checkScrollButtons);
    }, [featuredItems]);

    const fetchFeaturedItems = async () => {
        try {
            setLoading(true);
            const [hotelsResponse, eventsResponse, toursResponse] = await Promise.all([
                get("/api/accommodation/accommodation/"),
                get('/api/events/event/'),
                get('/api/tourism-info/destinations/')
            ]);

            let allItems = [];

            if (hotelsResponse.code === 200 && hotelsResponse.data) {
                allItems = allItems.concat(hotelsResponse.data.slice(0, 2).map(hotel => ({ ...hotel, type: 'hotel' })));
            }
            if (eventsResponse.code === 200 && eventsResponse.data) {
                allItems = allItems.concat(eventsResponse.data.slice(0, 2).map(event => ({ ...event, type: 'event' })));
            }
            if (toursResponse.code === 200 && toursResponse.data) {
                allItems = allItems.concat(toursResponse.data.slice(0, 2).map(tour => ({ ...tour, type: 'tour' })));
            }

            setFeaturedItems(allItems.sort(() => Math.random() - 0.5));
        } catch (err) {
            toast.error("获取精选推荐失败");
        } finally {
            setLoading(false);
        }
    };

    const scrollLeft = () => {
        featuredContainerRef.current.scrollBy({ left: -200, behavior: 'smooth' });
    };

    const scrollRight = () => {
        featuredContainerRef.current.scrollBy({ left: 200, behavior: 'smooth' });
    };

    const handleScroll = () => {
        if (featuredContainerRef.current) {
            const { scrollLeft, scrollWidth, clientWidth } = featuredContainerRef.current;
            setShowLeftButton(scrollLeft > 0);
            setShowRightButton(scrollLeft < scrollWidth - clientWidth - 1);
        }
    };

    const renderFeaturedItem = (item) => {
        switch (item.type) {
            case 'hotel':
                return (
                    <Link to={`/hotel/${item.id}`} className="block">
                        <div className="bg-white rounded-lg overflow-hidden shadow-lg transition duration-300 hover:shadow-xl">
                            <div className="relative">
                                <img src={`https://picsum.photos/seed/${item.id}/400/300`} alt={item.name} className="w-full h-48 object-cover" />
                                <div className="absolute top-0 right-0 bg-blue-500 text-white px-2 py-1 m-2 rounded-md text-sm font-semibold">
                                    {t('hotel')}
                                </div>
                            </div>
                            <div className="p-4">
                                <h3 className="text-xl font-bold mb-2 text-gray-800">{item.name}</h3>
                                <div className="flex items-center mb-2">
                                    <MapPinIcon className="h-5 w-5 text-gray-500 mr-1" />
                                    <span className="text-sm text-gray-600">{item.location}</span>
                                </div>
                                <div className="flex items-center">
                                    <StarIcon className="h-5 w-5 text-yellow-400 mr-1" />
                                    <span className="text-sm text-gray-600">{item.star_rating} {t('starRating')}</span>
                                </div>
                            </div>
                        </div>
                    </Link>
                );
            case 'event':
                return (
                    <Link to="/events" className="block">
                        <div className="bg-white rounded-lg overflow-hidden shadow-lg transition duration-300 hover:shadow-xl">
                            <div className="relative">
                                <img src={`https://picsum.photos/seed/${item.id}/400/300`} alt={item.name} className="w-full h-48 object-cover" />
                                <div className="absolute top-0 right-0 bg-green-500 text-white px-2 py-1 m-2 rounded-md text-sm font-semibold">
                                    {t('event')}
                                </div>
                            </div>
                            <div className="p-4">
                                <h3 className="text-xl font-bold mb-2 text-gray-800">{item.name}</h3>
                                <div className="flex items-center mb-2">
                                    <CalendarIcon className="h-5 w-5 text-gray-500 mr-1" />
                                    <span className="text-sm text-gray-600">{new Date(item.event_date).toLocaleDateString()}</span>
                                </div>
                                <div className="flex items-center">
                                    <MapPinIcon className="h-5 w-5 text-gray-500 mr-1" />
                                    <span className="text-sm text-gray-600">{item.venue}</span>
                                </div>
                            </div>
                        </div>
                    </Link>
                );
            case 'tour':
                return (
                    <Link to={`/tour/${item.id}`} className="block">
                        <div className="bg-white rounded-lg overflow-hidden shadow-lg transition duration-300 hover:shadow-xl">
                            <div className="relative">
                                <img src={`https://picsum.photos/seed/${item.id}/400/300`} alt={item.name} className="w-full h-48 object-cover" />
                                <div className="absolute top-0 right-0 bg-purple-500 text-white px-2 py-1 m-2 rounded-md text-sm font-semibold">
                                    {t('tour')}
                                </div>
                            </div>
                            <div className="p-4">
                                <h3 className="text-xl font-bold mb-2 text-gray-800">{item.name}</h3>
                                <div className="flex items-center mb-2">
                                    <TagIcon className="h-5 w-5 text-gray-500 mr-1" />
                                    <span className="text-sm text-gray-600">{item.category}</span>
                                </div>
                                <div className="flex items-center">
                                    <MapPinIcon className="h-5 w-5 text-gray-500 mr-1" />
                                    <span className="text-sm text-gray-600">{item.location}</span>
                                </div>
                            </div>
                        </div>
                    </Link>
                );
            default:
                return null;
        }
    };

    return (
        <div className="home-page bg-gray-100">
            {/* 欢迎部分 */}
            <section className="welcome-section bg-gradient-to-r from-blue-600 to-purple-600 py-24 text-center text-white relative overflow-hidden">
                <div className="absolute inset-0 bg-black opacity-50"></div>
                <div className="relative z-10">
                    <h1 className="text-5xl font-bold mb-4 animate-fade-in-down">{t('welcomeToTravely')}</h1>
                    <p className="text-2xl mb-8 animate-fade-in-up">{t('exploreWorldCreateMemories')}</p>
                    <Link
                        to="/tours"
                        className="bg-white text-blue-600 px-8 py-3 rounded-full text-lg font-semibold hover:bg-blue-100 transition duration-300 shadow-lg animate-pulse"
                    >
                        {t('startYourJourney')}
                    </Link>
                </div>
            </section>

            {/* 精选推荐 */}
            <section className="featured-items py-20 bg-white">
                <div className="container mx-auto px-4">
                    <h2 className="text-3xl font-bold mb-12 text-center text-gray-800">
                        {t('featuredRecommendations')}
                    </h2>
                    <div className="relative">
                        {showLeftButton && (
                            <button 
                                onClick={scrollLeft} 
                                className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white p-3 rounded-full shadow-md z-10 -ml-4 hover:bg-gray-100 transition duration-300"
                                aria-label="向左滚动"
                            >
                                <ChevronLeftIcon className="h-6 w-6 text-gray-600" />
                            </button>
                        )}
                        <div 
                            ref={featuredContainerRef} 
                            className="flex overflow-x-auto scrollbar-hide space-x-6 pb-4"
                            onScroll={handleScroll}
                        >
                            {featuredItems.map((item) => (
                                <div key={`${item.type}-${item.id}`} className="flex-none w-72">
                                    {renderFeaturedItem(item)}
                                </div>
                            ))}
                        </div>
                        {showRightButton && (
                            <button 
                                onClick={scrollRight} 
                                className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white p-3 rounded-full shadow-md z-10 -mr-4 hover:bg-gray-100 transition duration-300"
                                aria-label="向右滚动"
                            >
                                <ChevronRightIcon className="h-6 w-6 text-gray-600" />
                            </button>
                        )}
                    </div>
                </div>
            </section>

            {/* 特色部分 */}
            <section className="features py-20 bg-gray-100">
                <div className="container mx-auto px-4">
                    <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">{t('whyChooseTravely')}</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
                        <div className="text-center transform hover:scale-105 transition duration-300">
                            <div className="bg-blue-100 rounded-full p-6 inline-block mb-4">
                                <GlobeAltIcon className="h-12 w-12 text-blue-500" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2 text-gray-800">{t('globalDestinations')}</h3>
                            <p className="text-gray-600">{t('exploreWorldwideAttractions')}</p>
                        </div>
                        <div className="text-center transform hover:scale-105 transition duration-300">
                            <div className="bg-green-100 rounded-full p-6 inline-block mb-4">
                                <BoltIcon className="h-12 w-12 text-green-500" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2 text-gray-800">{t('quickBooking')}</h3>
                            <p className="text-gray-600">{t('simpleBookingProcess')}</p>
                        </div>
                        <div className="text-center transform hover:scale-105 transition duration-300">
                            <div className="bg-purple-100 rounded-full p-6 inline-block mb-4">
                                <SparklesIcon className="h-12 w-12 text-purple-500" />
                            </div>
                            <h3 className="text-xl font-semibold mb-2 text-gray-800">{t('qualityExperience')}</h3>
                            <p className="text-gray-600">{t('carefullySelectedServices')}</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* 关于我们 */}
            <section className="about-us py-20 bg-blue-50">
                <div className="container mx-auto px-4 text-center">
                    <h2 className="text-3xl font-bold mb-6 text-gray-800">
                        {t('aboutTravely')}
                    </h2>
                    <p className="max-w-2xl mx-auto text-gray-600 mb-10 text-lg leading-relaxed">
                        {t('aboutTravelyDescription')}
                    </p>
                    <Link
                        to="/about"
                        className="bg-blue-600 text-white px-8 py-3 rounded-full hover:bg-blue-700 transition duration-300 inline-block text-lg font-semibold shadow-lg"
                    >
                        {t('learnMoreAboutUs')}
                    </Link>
                </div>
            </section>
        </div>
    );
};

export default Home;