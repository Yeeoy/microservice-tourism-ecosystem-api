import React, { useContext, useState, useRef } from "react";
import { Link, useLocation } from "react-router-dom";
import { AuthContext } from "../../context/authContext";
import { useTranslation } from 'react-i18next';
import {
    Avatar,
    Popper,
    Paper,
    MenuList,
    MenuItem,
    ClickAwayListener,
    Grow,
    Button,
} from "@mui/material";
import {
    AccountCircle,
    ExitToApp,
    Hotel,
    Event,
    Map,
    DirectionsCar,
    Restaurant,
    EventSeat,
    Language,
} from "@mui/icons-material";

const Navbar = () => {
    const { user, logout } = useContext(AuthContext);
    const [open, setOpen] = useState(false);
    const [langMenuOpen, setLangMenuOpen] = useState(false);
    const anchorRef = useRef(null);
    const langAnchorRef = useRef(null);
    const location = useLocation();
    const { t, i18n } = useTranslation();

    const handleToggle = () => {
        setOpen((prevOpen) => !prevOpen);
    };

    const handleClose = (event) => {
        if (anchorRef.current && anchorRef.current.contains(event.target)) {
            return;
        }
        setOpen(false);
    };

    const handleListKeyDown = (event) => {
        if (event.key === "Tab") {
            event.preventDefault();
            setOpen(false);
        } else if (event.key === "Escape") {
            setOpen(false);
        }
    };

    const handleLogout = () => {
        logout();
        setOpen(false);
    };

    const isActive = (path) => {
        return location.pathname === path
            ? "text-blue-600"
            : "text-gray-800 hover:text-blue-600";
    };

    const changeLanguage = (lng) => {
        i18n.changeLanguage(lng);
        setLangMenuOpen(false);
    };

    const handleLangMenuToggle = () => {
        setLangMenuOpen((prevOpen) => !prevOpen);
    };

    const handleLangMenuClose = (event) => {
        if (langAnchorRef.current && langAnchorRef.current.contains(event.target)) {
            return;
        }
        setLangMenuOpen(false);
    };

    return (
        <nav className="bg-white fixed top-0 left-0 right-0 z-50 shadow-sm">
            <div className="container mx-auto flex justify-between items-center py-4 px-6">
                <Link to="/" className="text-gray-800 text-2xl font-bold">
                    Travely
                </Link>
                <div className="flex items-center space-x-6">
                    <ul className="flex space-x-6">
                        <li>
                            <Link
                                to="/"
                                className={`transition duration-300 ${isActive(
                                    "/"
                                )}`}>
                                {t('home')}
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/hotels"
                                className={`transition duration-300 ${isActive(
                                    "/hotels"
                                )}`}>
                                {t('hotels')}
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/events"
                                className={`transition duration-300 ${isActive(
                                    "/events"
                                )}`}>
                                {t('events')}
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/tours"
                                className={`transition duration-300 ${isActive(
                                    "/tours"
                                )}`}>
                                {t('tours')}
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/transportation"
                                className={`transition duration-300 ${isActive(
                                    "/transportation"
                                )}`}>
                                {t('transportation')}
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/restaurants"
                                className={`transition duration-300 ${isActive(
                                    "/restaurants"
                                )}`}>
                                {t('restaurants')}
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/about"
                                className={`transition duration-300 ${isActive(
                                    "/about"
                                )}`}>
                                {t('about')}
                            </Link>
                        </li>
                    </ul>
                    <div>
                        <Button
                            ref={langAnchorRef}
                            onClick={handleLangMenuToggle}
                            startIcon={<Language />}
                        >
                            {i18n.language === 'zh' ? '中文' : 'English'}
                        </Button>
                        <Popper
                            open={langMenuOpen}
                            anchorEl={langAnchorRef.current}
                            role={undefined}
                            placement="bottom-start"
                            transition
                            disablePortal
                        >
                            {({ TransitionProps, placement }) => (
                                <Grow
                                    {...TransitionProps}
                                    style={{
                                        transformOrigin:
                                            placement === 'bottom-start' ? 'left top' : 'left bottom',
                                    }}
                                >
                                    <Paper>
                                        <ClickAwayListener onClickAway={handleLangMenuClose}>
                                            <MenuList autoFocusItem={langMenuOpen} id="language-menu">
                                                <MenuItem onClick={() => changeLanguage('zh')}>中文</MenuItem>
                                                <MenuItem onClick={() => changeLanguage('en')}>English</MenuItem>
                                            </MenuList>
                                        </ClickAwayListener>
                                    </Paper>
                                </Grow>
                            )}
                        </Popper>
                    </div>
                    {user ? (
                        <div
                            ref={anchorRef}
                            onMouseEnter={() => setOpen(true)}
                            onMouseLeave={() => setOpen(false)}>
                            <Avatar
                                src={
                                    user.avatar || "/images/default-avatar.png"
                                }
                                alt="User Avatar"
                            />
                            <Popper
                                open={open}
                                anchorEl={anchorRef.current}
                                role={undefined}
                                placement="bottom-end"
                                transition
                                disablePortal
                                style={{ zIndex: 1000 }}>
                                {({ TransitionProps, placement }) => (
                                    <Grow
                                        {...TransitionProps}
                                        style={{
                                            transformOrigin:
                                                placement === "bottom"
                                                    ? "center top"
                                                    : "center bottom",
                                        }}>
                                        <Paper>
                                            <ClickAwayListener onClickAway={handleClose}>
                                                <MenuList
                                                    autoFocusItem={open}
                                                    id="menu-list-grow"
                                                    onKeyDown={
                                                        handleListKeyDown
                                                    }>
                                                    <MenuItem
                                                        onClick={handleClose}
                                                        component={Link}
                                                        to="/profile">
                                                        <AccountCircle className="mr-2" />
                                                        {t('profile')}
                                                    </MenuItem>
                                                    <MenuItem
                                                        onClick={handleClose}
                                                        component={Link}
                                                        to="/hotel-orders">
                                                        <Hotel className="mr-2" />
                                                        {t('hotelOrders')}
                                                    </MenuItem>
                                                    <MenuItem
                                                        onClick={handleClose}
                                                        component={Link}
                                                        to="/event-orders">
                                                        <Event className="mr-2" />
                                                        {t('eventOrders')}
                                                    </MenuItem>
                                                    <MenuItem
                                                        onClick={handleClose}
                                                        component={Link}
                                                        to="/tour-orders">
                                                        <Map className="mr-2" />
                                                        {t('tourOrders')}
                                                    </MenuItem>
                                                    <MenuItem
                                                        onClick={handleClose}
                                                        component={Link}
                                                        to="/ride-orders">
                                                        <DirectionsCar className="mr-2" />
                                                        {t('rideOrders')}
                                                    </MenuItem>
                                                    <MenuItem
                                                        onClick={handleClose}
                                                        component={Link}
                                                        to="/restaurant-orders">
                                                        <Restaurant className="mr-2" />
                                                        {t('restaurantOrders')}
                                                    </MenuItem>
                                                    <MenuItem
                                                        onClick={handleClose}
                                                        component={Link}
                                                        to="/table-reservations">
                                                        <EventSeat className="mr-2" />
                                                        {t('tableReservations')}
                                                    </MenuItem>
                                                    <MenuItem
                                                        onClick={handleLogout}>
                                                        <ExitToApp className="mr-2" />
                                                        {t('logout')}
                                                    </MenuItem>
                                                </MenuList>
                                            </ClickAwayListener>
                                        </Paper>
                                    </Grow>
                                )}
                            </Popper>
                        </div>
                    ) : (
                        <div className="flex space-x-2">
                            <Link
                                to="/login"
                                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition duration-300">
                                {t('login')}
                            </Link>
                            <Link
                                to="/register"
                                className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 transition duration-300">
                                {t('register')}
                            </Link>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
