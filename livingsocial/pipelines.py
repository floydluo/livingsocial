#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).

Scrapy pipeline part - stores scraped items in the database.
"""

from sqlalchemy.orm import sessionmaker
from livingsocial.models import Deals, db_connect, create_deals_table


class LivingsocialPipeline(object):
    """Livingsocial pipeline for storing scraped items in the database"""
    


    def __init__(self):
        """Initializes database connection and sessionmaker.

        Creates deals table.

        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)
        

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        
        session = self.Session()
        deal = Deals(**item)

        try:
            session.add(deal)

            # The author use commit() here, this is interesting.
            # session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.commit()
            session.close()
        

        return item
        # Put them to terminal
