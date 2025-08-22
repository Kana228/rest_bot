"""
Tests for bot handlers
"""
import pytest
from unittest.mock import Mock, AsyncMock
from aiogram.types import Message, CallbackQuery, User, Chat

from handlers.cart_handler import CartHandler
from handlers.menu_handler import MenuHandler
from handlers.order_handler import OrderHandler


class TestCartHandler:
    """Test cart handler functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.bot = Mock()
        self.dp = Mock()
        self.handler = CartHandler(self.bot, self.dp)
    
    def test_register_handlers(self):
        """Test that handlers are properly registered"""
        self.handler.register_handlers()
        assert self.dp.message.register.called
        assert self.dp.callback_query.register.called


class TestMenuHandler:
    """Test menu handler functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.bot = Mock()
        self.dp = Mock()
        self.handler = MenuHandler(self.bot, self.dp)
    
    def test_register_handlers(self):
        """Test that handlers are properly registered"""
        self.handler.register_handlers()
        assert self.dp.message.register.called
        assert self.dp.callback_query.register.called


class TestOrderHandler:
    """Test order handler functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.bot = Mock()
        self.dp = Mock()
        self.handler = OrderHandler(self.bot, self.dp)
    
    def test_register_handlers(self):
        """Test that handlers are properly registered"""
        self.handler.register_handlers()
        assert self.dp.message.register.called
        assert self.dp.callback_query.register.called
