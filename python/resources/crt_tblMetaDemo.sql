USE [demosource]
GO

/****** Object:  Table [dbo].[tblMetaDemo]    Script Date: 8/29/2020 11:35:01 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tblMetaDemo](
	[UUID] [nchar](36) NOT NULL,
	[Id] [nchar](36) NOT NULL,
	[Version] [nchar](10) NOT NULL,
	[Type] [nchar](10) NOT NULL,
	[Description] [nchar](100) NULL,
	[Status] [nchar](10) NOT NULL,
	[ActiveFrom] [time](7) NULL,
	[ActiveUntil] [time](7) NULL,
 CONSTRAINT [PK_tblMetaDemo] PRIMARY KEY CLUSTERED 
(
	[UUID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

